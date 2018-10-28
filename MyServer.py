from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        pass

    
    def do_GET(self):
        pass


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()