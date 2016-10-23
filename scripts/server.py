import os
import SimpleHTTPServer
import SocketServer
import webbrowser
try: 
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", 8000), Handler)
    httpd.serve_forever()
except KeyboardInterrupt: 
    httpd.shutdown()
    httpd.server_close()
