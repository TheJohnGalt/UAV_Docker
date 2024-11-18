import http.server
import socketserver
from PIL import Image
import io

PORT = 9000

class ImageHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/image':
            img = Image.open('test.jpg')
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0) 
            
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            
            self.wfile.write(img_byte_arr.getvalue())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

with socketserver.TCPServer(("", PORT), ImageHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()