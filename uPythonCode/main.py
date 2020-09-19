import socket, machine, uasyncio

import http_server


class LEDStripServer(http_server.HTTPServer):
    def __init__(self):
        """Setup pins and pwm objects"""

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

        if not data_dict["mode"] in ["switch", "analog"]:
            await self.bad_request(reader, writer, data_dict)
            return

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

        await writer.awrite("HTTP/1.0 200 OK\r\n")

        await reader.aclose()
        await writer.aclose()

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
    loop = uasyncio.get_event_loop()

    loop.create_task(led_strip_server.start_server())
    loop.create_task(heartbeat())
    loop.run_forever()


if __name__ == "__main__":
    main()
