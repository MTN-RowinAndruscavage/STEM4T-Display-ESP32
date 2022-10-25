## Creates a Wifi access point
## Serves a web page with the device's name and a random fortune cookie

ap_ssid="TDweb-%s" % username
ap_password="5GforAll"

fortunes = [
    "This is the first",
    "Have fortune #2",
    "Third time is a charm"
]

import network

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ap_ssid, password=ap_password)

try:
  import usocket as socket
except:
  import socket

import esp
esp.osdebug(None)

import random
import gc
gc.collect()

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())
TD.clear()
TD.typeset("SSID: %s\nPW: %s\nhttp://%s/" % (ap_ssid, ap_password, ap.ifconfig()[0]))

def web_page():
  html = """<html><head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
  <h1>Welcome to %s's server</h1>
  %s
  </body>
  </html>""" % (username, random.choice(fortunes))
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Display web hits
webcounter = 0

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()
  
  webcounter += 1
  TD.typeset("Page views: %d" % webcounter, 0, 3)
  TD.typeset("Last from: %s" % addr[0], 0, 4)