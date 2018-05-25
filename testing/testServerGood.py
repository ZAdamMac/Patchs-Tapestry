# A simple HTTPS server to test the ability of Tapestry to appropriately accept a good connection.

# TODO should be enhanced to support a loom-like upload and download

import http.server as hs
import ssl

httpd = hs.HTTPServer(('localhost', 49153), hs.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./goodCert.pem', server_side=True)
httpd.serve_forever()