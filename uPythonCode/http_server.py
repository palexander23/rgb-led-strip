import uasyncio, ure


class HTTPServer:
    def __init__(self):

        self.debug = False

        # Group three of the match will give the number without the white space
        self.content_length_regex = ure.compile("(.+)(\s)([0-9]+)")

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

        # Get and print IP Address
        self.ip_address = self.wlan.ifconfig()[0]
        print("IP Address: {}".format(self.ip_address))

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

        # Define a default body length if it cannot be decoded from the req head
        body_len = 1024

        try:
            # Look for the content length number in the request head
            match = self.content_length_regex.match(head)

            # Extract that value without the whitespace
            body_len_str = match.group(3)
            body_len = int(body_len_str)

        except Exception as e:
            print("Could not decode the content length: {}".format(e))

        if req_type == "POST":
            await self.process_post(reader, writer, head, body_len)

        if req_type == "GET ":
            self.process_get(reader, writer, head, body_len)

        if req_type == "PUT ":
            self.process_put(reader, writer, head, body_len)

    async def process_get(self, reader, writer, head, body_len):
        """###STUB###
        Begin the processing of a get request.
        """

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    async def process_put(self, reader, writer, head, body_len):
        """###STUB###
        Begin the processing of a put request.
        """

        soc.send("HTTP/1.0 200 OK\r\n")
        soc.close()

    async def process_post(self, reader, writer, head, body_len):
        """Begin processing of put request.
        Populate dict with key value pairs in post request body and pass dict
        to virtual method post_handler()
        """
        import ujson

        try:
            body_bytes = await reader.read(body_len)

        except StopIteration:
            print("Could not retrieve body")

        body = body_bytes.decode()

        try:
            body_dict = ujson.loads(body)

        except Exception as e:
            await self.bad_request(reader, writer, {})
            print("Body Javascript Decode Error: {}".format(e))
            print("Body Received:")
            print(body)

            return

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

    async def bad_request(self, reader, writer, data_dict):
        pass
