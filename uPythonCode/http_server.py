import uasyncio


class HTTPServer:
    def __init__(self):

        self.debug = False

        self.wifi_connect()

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

    async def start_server(self):
        server = await uasyncio.start_server(self.handle_request, "0.0.0.0", 80)
        await server.serve_forever()

    async def handle_request(self, reader, writer):

        head = b""
        r = b""

        while r != b"\r\n":
            r = await reader.readline()
            head += r

        head = head.decode()

        req_type = head[0:4]

        if req_type == "POST":
            await self.process_post(reader, writer, head)

        if req_type == "GET ":
            self.process_get(reader, writer, head)

        if req_type == "PUT ":
            self.process_put(reader, writer, head)

    async def process_get(self, reader, writer, head):
        """###STUB###
        Begin the processing of a get request.
        """

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    async def process_put(self, reader, writer, head):
        """###STUB###
        Begin the processing of a put request.
        """

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    async def process_post(self, reader, writer, head):
        """Begin processing of put request.
        Populate dict with key value pairs in post request body and pass dict
        to virtual method post_handler()
        """
        import ujson

        try:
            body_bytes = await reader.read(100)
        except StopIteration:
            print("Could not retrieve body")

        body = body_bytes.decode()
        body_dict = ujson.loads(body)

        await self.post_handler(body_dict, reader, writer)

    async def post_handler(self, data_dict, reader, writer):
        """Stub for overriding by subclassing HTTPServer.
        For code used to handle post requests. 
        Socket passed as soc should have a HTTP response sent and should
        be closed after transaction is completed.
        """
        pass

    async def post_req_debug_out(self, data_dict):
        """Prints POST request data to the UART terminal if instance variable debug
        is True.
        """

        if not self.debug:
            return

        print(data_dict)
