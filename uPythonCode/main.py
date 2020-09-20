import socket, machine, uasyncio, ure

import http_server


loop = uasyncio.get_event_loop()


class LEDStripServer(http_server.HTTPServer):
    def __init__(self):
        """Setup pins and pwm objects"""

        # Set up regex object to find colour hex strings
        self.colour_hex_decoder = ure.compile("^#[A-Fa-f0-9]+$")

        super().__init__()

        self.red_pin = machine.Pin(4)
        self.gre_pin = machine.Pin(16)
        self.blu_pin = machine.Pin(17)

        self.red_pwm = machine.PWM(self.red_pin)
        self.red_pwm.duty(0)

        self.gre_pwm = machine.PWM(self.gre_pin)
        self.gre_pwm.duty(0)

        self.blu_pwm = machine.PWM(self.blu_pin)
        self.blu_pwm.duty(0)

        self.pwm_objects = [self.red_pwm, self.blu_pwm, self.gre_pwm]

        for pwm in self.pwm_objects:
            pwm.freq(1000)

        self.debug = True

        self.active_task = None

    async def post_handler(self, data_dict, reader, writer):
        """Sets the behaviour of the LEDS.
        Looks for a mode then looks for further bits of post data to determine
        LED State.

        Modes:
            * switch: 
                - POST data:
                    - red = ON/OFF
                    - gre = ON/OFF
                    - blu = ON/OFF

            * analog:
                - POST data:
                    - red = int(0, 1023)
                    - gre = int(0, 1023)
                    - blu = int(0, 1023)
        """
        if not "mode" in data_dict:
            await self.bad_request(reader, writer, data_dict)
            return

        if not data_dict["mode"] in ["switch", "analog", "flash", "fade"]:
            await self.bad_request(reader, writer, data_dict)
            return

        if self.active_task != None:
            self.active_task.cancel()
            self.active_task = None

        if data_dict["mode"] == "switch":
            for led, pwm_obj in zip(["red", "gre", "blu"], self.pwm_objects):
                if data_dict[led] == "ON":
                    pwm_obj.duty(1023)
                elif data_dict[led] == "OFF":
                    pwm_obj.duty(0)
                else:
                    await self.bad_request(reader, writer, data_dict)
                    return

        if data_dict["mode"] == "analog":
            for led, pwm_obj in zip(["red", "gre", "blu"], self.pwm_objects):
                try:
                    pwm_int = int(data_dict[led])
                except:
                    await self.bad_request(reader, writer, data_dict)
                    return

                pwm_obj.duty(pwm_int)

        if data_dict["mode"] == "flash":
            colour_list = data_dict["colour_list"]
            on_time_list = data_dict["on_time_list"]

            if len(colour_list) != len(on_time_list) or len(colour_list) < 2:
                await self.bad_request(reader, writer, data_dict)
                return

            self.active_task = loop.create_task(
                self.flash_task(colour_list, on_time_list, reader, writer, data_dict)
            )

        if data_dict["mode"] == "fade":
            colour_list = data_dict["colour_list"]
            on_time_list = data_dict["on_time_list"]
            fade_time_list = data_dict["fade_time_list"]

            if (
                not len(colour_list) == len(on_time_list) == len(fade_time_list)
                or len(colour_list) < 2
            ):
                self.bad_request(reader, writer, data_dict)

            self.active_task = loop.create_task(
                self.fade_task(
                    colour_list, on_time_list, fade_time_list, reader, writer, data_dict
                )
            )

        await writer.awrite("HTTP/1.0 200 OK\r\n")

        await reader.aclose()
        await writer.aclose()

    async def flash_task(self, colours_list, on_times_list, reader, writer, data_dict):
        try:
            while True:
                for colour, time in zip(colours_list, on_times_list):
                    rgb_vals = await self.decode_hex_colour(colour)

                    if rgb_vals == []:
                        await self.bad_request(reader, writer, data_dict)
                        return

                    mapped_vals = []

                    for val in rgb_vals:
                        mapped_val = await self.map(val, 0, 255, 0, 1023)
                        mapped_vals.append(mapped_val)

                    for mapped_val, pwm_obj in zip(mapped_vals, self.pwm_objects):
                        pwm_obj.duty(mapped_val)

                    await uasyncio.sleep(float(time))

        except uasyncio.CancelledError:
            raise

    async def fade_task(
        self, colour_list, on_time_list, fade_time_list, reader, writer, data_dict
    ):
        try:
            while True:
                for idx, (curr_col, on_time, fade_time) in enumerate(
                    zip(colour_list, on_time_list, fade_time_list)
                ):

                    # Get index of next colour
                    next_idx = idx + 1
                    if next_idx > len(colour_list) - 1:
                        next_idx = 0

                    # Set LED vals for on time
                    curr_rgb_vals = await self.decode_hex_colour(curr_col)

                    if curr_rgb_vals == []:
                        await self.bad_request(reader, writer, data_dict)
                        return

                    mapped_curr_vals = []

                    for curr_val in curr_rgb_vals:
                        mapped_curr_val = await self.map(curr_val, 0, 255, 0, 1023)
                        mapped_curr_vals.append(mapped_curr_val)

                    for mapped_curr_val, pwm_obj in zip(
                        mapped_curr_vals, self.pwm_objects
                    ):
                        pwm_obj.duty(mapped_curr_val)

                    await uasyncio.sleep(float(on_time))

                    # Set up the fade

                    # Get number of 60th of a second second increments that occur
                    # during the fade operation
                    fade_refresh_rate = 60

                    num_incr = round(float(fade_time) * fade_refresh_rate)

                    next_col = colour_list[next_idx]
                    next_rgb_vals = await self.decode_hex_colour(next_col)

                    rgb_diffs = [
                        next_val - curr_val
                        for next_val, curr_val in zip(next_rgb_vals, curr_rgb_vals)
                    ]

                    # Run the fade
                    for count in range(num_incr):

                        # Calculate this count's LED values
                        fade_vals = [
                            curr_rgb_val + (rgb_diff * count / num_incr)
                            for rgb_diff, curr_rgb_val in zip(rgb_diffs, curr_rgb_vals)
                        ]

                        # Apply these LED values to the strip
                        mapped_fade_vals = []

                        for fade_val in fade_vals:
                            mapped_val = round(
                                await self.map(fade_val, 0, 255, 0, 1023)
                            )
                            mapped_fade_vals.append(mapped_val)

                        for val, pwm_obj in zip(mapped_fade_vals, self.pwm_objects):
                            pwm_obj.duty(val)

                        # Wait for the next increment
                        await uasyncio.sleep(1 / fade_refresh_rate)

        except uasyncio.CancelledError:
            raise

    async def decode_hex_colour(self, hex_str):
        """Get three ints corresponding to the r, g and b values encoded in a standard
        colour hex: #RRGGBB
        
        :param hex_str: the hex string to decode.
        :type hex_str: str

        :return: A list of ints [r, g, b] if correct format. An empty list if incorrect
            format.
        :rtype: List[]
        """

        try:
            match = self.colour_hex_decoder.match(hex_str)
            if not len(match.group(0)) == len(hex_str) == 7:
                return []

        except:
            return []

        # The hex string is the correct format, time to decode
        red = int(hex_str[1:3], 16)
        gre = int(hex_str[3:5], 16)
        blu = int(hex_str[5:7], 16)

        return [red, gre, blu]

    async def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    async def bad_request(self, reader, writer, data_dict):

        await writer.awrite("HTTP/1.0 400 BAD REQUEST\r\n")

        await reader.aclose()
        await writer.aclose()

        await self.post_req_debug_out(data_dict)


async def heartbeat():
    """Flash the onboard LED in a heartbeat to show the event loop is running"""

    from machine import Pin

    status_led = Pin(2, Pin.OUT)

    status_led.on()
    await uasyncio.sleep(0.1)
    status_led.off()
    await uasyncio.sleep(0.1)

    status_led.on()
    await uasyncio.sleep(0.1)
    status_led.off()
    await uasyncio.sleep(0.1)

    while True:
        status_led.on()
        await uasyncio.sleep(0.5)
        status_led.off()
        await uasyncio.sleep(0.5)


def main():
    led_strip_server = LEDStripServer()

    # Set up event loop
    loop.create_task(led_strip_server.start_server())
    loop.create_task(heartbeat())
    loop.run_forever()


if __name__ == "__main__":
    main()
