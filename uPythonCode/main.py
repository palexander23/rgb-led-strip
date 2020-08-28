import socket, machine

import http_server


class LEDStripServer(http_server.HTTPServer):
    def __init__(self):
        """Setup pins and pwm objects"""

        super().__init__()

        self.red_pin = machine.Pin(4)
        self.gre_pin = machine.Pin(16)
        self.blu_pin = machine.Pin(17)

        self.red_pwm = machine.PWM(self.red_pin)
        self.gre_pwm = machine.PWM(self.gre_pin)
        self.blu_pwm = machine.PWM(self.blu_pin)

        self.pwm_objects = [self.red_pwm, self.blu_pwm, self.gre_pwm]

        for pwm in self.pwm_objects:
            pwm.freq(1000)
            pwm.duty(0)

    def post_handler(self, data_dict, soc):
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
            self.bad_request(soc)
            return

        if not data_dict["mode"] in ["switch", "analog"]:
            self.bad_request(soc)
            return

        if data_dict["mode"] == "switch":
            for led, pwm_obj in zip(["red", "gre", "blu"], self.pwm_objects):
                if data_dict[led] == "ON":
                    pwm_obj.duty(1023)
                elif data_dict[led] == "OFF":
                    pwm_obj.duty(0)
                else:
                    self.bad_request(soc)
                    return

        if data_dict["mode"] == "analog":
            for led, pwm_obj in zip(["red", "gre", "blu"], self.pwm_objects):
                try:
                    pwm_int = int(data_dict[led])
                except:
                    self.bad_request(soc)
                    return

                pwm_obj.duty(pwm_int)

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    def bad_request(self, soc):
        soc.send("HTTP/1.0 400 BAD REQUEST\r\n")
        soc.close()


def main():
    led_strip_server = LEDStripServer()

    led_strip_server.request_loop()

if __name__ == "__main__":
    main()
