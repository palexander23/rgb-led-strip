class HTTPServer:
    def __init__(self):
        from machine import Pin

        self.status_led = Pin(2, Pin.OUT)

        self.debug = False

        self.wifi_connect()
        self.setup_socket()

    def wifi_connect(self):
        """Establish WIFI connection with details stored in separate file"""

        import network
        import wifi_details

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        get_wifi_details = wifi_details.get_wifi_details
        if not self.wlan.isconnected():
            name, psk = get_wifi_details()
            self.wlan.connect(name, psk)

            while not self.wlan.isconnected():
                pass

    def setup_socket(self):
        import socket

        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

        self.soc = socket.socket()
        self.soc.bind(addr)
        self.soc.listen(1)

    def request_loop(self):
        while True:
            cl, addr = self.soc.accept()
            self.status_led.on()

            head = b""
            r = b""

            while r != b"\r\n":
                r = cl.readline()
                head += r

            head = head.decode()

            req_type = head[0:4]

            self.status_led.off()

            if req_type == "POST":
                self.process_post(cl, head)

            if req_type == "GET ":
                self.process_get(cl, head)

            if req_type == "PUT ":
                self.process_put(cl, head)

    def process_get(self, soc, head):
        """###STUB###
        Begin the processing of a get request.
        """

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    def process_put(self, soc, head):
        """###STUB###
        Begin the processing of a put request.
        """

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    def process_post(self, soc, head):
        """Begin processing of put request.
        Populate dict with key value pairs in post request body and pass dict
        to virtual method post_handler()
        """
        import ujson

        body = soc.recv(1024).decode()
        body_dict = ujson.loads(body)

        self.post_handler(body_dict, soc)

    def post_handler(self, data_dict, soc):
        """Stub for overriding by subclassing HTTPServer.
        For code used to handle post requests. 
        Socket passed as soc should have a HTTP response sent and should
        be closed after transaction is completed.
        """
        pass

    def post_req_debug_out(self, data_dict):
        """Prints POST request data to the UART terminal if instance variable debug
        is True.
        """

        if not self.debug:
            return

        print(data_dict)

