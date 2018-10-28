#!/usr/bin/env python3
#
# An HTTP server that remembers your name (in a cookie)

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
from urllib.parse import parse_qs
from html import escape as html_escape

form = '''<!DOCTYPE html>
<title>I Know Age</title>
<p>
{}
<p>
<form method="POST">
<label>What's your age?
<input type="text" name="age">
</label>
<br>
<button type="submit">Tell me!</button>
</form>
'''


class AgeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
    
        length = int(self.headers.get('Content-length', 0))
        data = self.rfile.read(length).decode()
        age = parse_qs(data)["age"][0]

        # Create cookie.
        c = cookies.SimpleCookie()
        c['age'] = age
        c['age']['domain'] = 'localhost'
        c['age']['max-age'] = 70

        # Send a 303 back to the root page, with a cookie!
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', c['age'].OutputString())
        self.end_headers()

    def do_GET(self):
        
        message = "I don't know your age!"

        # Look for a cookie in the request.
        if 'cookie' in self.headers:
            try:
                c = cookies.SimpleCookie(self.headers['cookie'])
                age = c['age'].value

                # Craft a message, escaping any HTML special chars in name.
                message = "Hey there, your age is " + html_escape(age)
            except (KeyError, cookies.CookieError) as e:
                message = "I'm not sure about your age!"
                print(e)

        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Send the form with the message in it.
        mesg = form.format(message)
        self.wfile.write(mesg.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, AgeHandler)
    httpd.serve_forever()
