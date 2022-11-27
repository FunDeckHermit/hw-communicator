from http.server import BaseHTTPRequestHandler,HTTPServer
from datetime import datetime
from threading import Thread

PORT = 8000
ActiveLED = 0
SetTime = datetime.utcnow()

def trysetLED(stripped):
    global ActiveLED, SetTime
    ActiveLED = int(stripped)
    SetTime = datetime.utcnow()
    print(f"ActiveLED set {ActiveLED} with ts {SetTime}")
    

def checkTimeout():
    global ActiveLED, SetTime
    if ActiveLED > 0:
        if (datetime.utcnow() - SetTime).total_seconds() > 5 * 60:
            print("Time passed, activeLED reset")
            SetTime = datetime.utcnow()
            ActiveLED = 0


class RandomNumber(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            led = self.path.split('/')[1]
            guid = self.path.split('/')[2]
            trysetLED(led)
        except ValueError:
            seconds = (datetime.utcnow() - SetTime).total_seconds() 
            print(f"Value not set for {seconds:.0f} seconds")
        except IndexError:
            return
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        checkTimeout()
            
        self.wfile.write(f"{ActiveLED}".encode())
        return

class MyServer(HTTPServer):
    def service_actions(self):
        now = datetime.utcnow()
        delta = now - starttime
        if ActiveLED == 0:
            if delta.total_seconds() > 60*12:
                thread = Thread(target=self.shutdown)
                thread.start()

print("starting server")
starttime = datetime.utcnow()
server = MyServer(("", PORT), RandomNumber)
server.serve_forever()
print("server stopped")

