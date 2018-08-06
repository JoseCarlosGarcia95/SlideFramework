def run_module(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json; charset=utf-8')
    self.end_headers()
    
    self.wfile.write(str.encode('{"text" : "Hola mundo"}'))
