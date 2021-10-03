import wifi
import usocket as socket
import time
import re
import gc
gc.collect()


waitForConnectionTimeout = 10


class ConfigChanger:
    def __init__(self, config, display):
        self.config = config
        self.display = display
        self.waitForConnection = 0
        self.finished = False
        self.connectionSuccessful = False

    def __getResponse(self):
        if self.finished:
            return self.__getFinishedPage()
        elif self.__isTestingConnection():
            return self.__getTestingPage()
        else:
            return self.__getConfigPage()
        
    def __isTestingConnection(self):
        if not self.connectionSuccessful:
            self.connectionSuccessful = wifi.isConnected()
        
        if  time.time() > self.waitForConnection or self.connectionSuccessful:
            wifi.disconnect()
            return False
        else:
            return True

    def __getTestingPage(self):
        return '''
      <html>
      <head>
          <title>Testing WiFi connection...</title>
          <meta http-equiv="refresh" content="3; URL=/" />
      </head>
      <body>
          <h1>Testing WiFi connection...</h1>
      </body>
      </html>

      '''
    
    def __getFinishedPage(self):
        return '''
      <html>
      <head>
          <title>Finished</title>
          <meta http-equiv="refresh" content="3; URL=/" />
      </head>
      <body>
          <h1>Finished.</h1>
      </body>
      </html>

      '''

    def __getConfigPage(self):
        html = '''
  <!DOCTYPE html>
  <html>
  <body>

  <h1>Rainradar</h1>

  <h2>Status</h2>

  <p>WiFi: ''' + {True: '<span style="color:green;">Connected</span>',
               False: '<span style="color:red;">Not connected</span>'}[self.connectionSuccessful] + '''
  </p>

  <p>
  <form action="/">
     <input type="hidden" id="retest" name="retest" value="">
     <input type="submit" value="Retest">
  </form>
  </p>
  
  <h2>Config</h2>
  <p>
  <form action="/">
    <label for="fname">WiFi Name (SSID):</label><br>
    <input type="text" id="ssid" name="ssid" value="''' + self.config.getSsid() + '''"><br>
    <label for="fname">WiFi Password (SSID):</label><br>
    <input type="text" id="password" name="password" value="''' + self.config.getPassword() + '''"><br>
    <label for="fname">Postal Index:</label><br>
    <input type="text" id="plz" name="plz" value="''' + self.config.getPlz() + '''"><br>
    <input type="submit" value="Save changes">
  </form> 
  </p>
  
  <h2>Available WiFi's</h2>
  <p>
  ''' + '<br>'.join(wifi.listNetworks()) + '''
  </p>

  <p>
  <form action="/">
     <input type="hidden" id="finish" name="finish" value="">
     <input type="submit" value="Exit Config">
  </form>
  </p>

  </body>
  </html>
    '''
        return html

    def __updateConfigFromRequest(self, request):
        containsQueryParameters = False
        changed = False
        testConnection = False
        print(request)
        split1 = request.split('\n')[0].split(' ')[1].split('?')
        if len(split1) > 1:
            containsQueryParameters = True
            for paramValue in split1[1].split('&'):
                if '=' in paramValue:
                    param, value = paramValue.split('=')
                else:
                    param = paramValue
                    value = ''
                if param == 'ssid' and value != self.config.getSsid():
                    self.config.setSsid(value)
                    changed = True
                    testConnection = True
                elif param == 'password' and value != self.config.getPassword():
                    self.config.setPassword(value)
                    changed = True
                    testConnection = True
                elif param == 'plz' and value != self.config.getPlz():
                    self.config.setPlz(value)
                    changed = True
                elif param == 'retest':
                    testConnection = True
                elif param == 'finish':
                    self.finished = True
        if changed:
            self.config.writeConfig()
        if testConnection:
            self.__testWifiConnection()
        return containsQueryParameters


    def __testWifiConnection(self):
        self.connectionSuccessful = False
        wifi.connect(self.config.getSsid(), self.config.getPassword(), wait=False)
        self.waitForConnection = time.time() + waitForConnectionTimeout


    def startServer(self):
        self.display.showText("CONF")
        wifi.startAccessPoint()
        self.__testWifiConnection()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        s.listen(1)

        while not self.finished:
            try:
                conn, addr = s.accept()
                conn.settimeout(3.0)
                print('Got a connection from %s' % str(addr))
                request = str(conn.recv(1024))
                conn.settimeout(None)
                if self.__updateConfigFromRequest(request):
                    conn.send('HTTP/1.1 303 See Other\n')
                    conn.send('Location: ./\n')
                else:
                    conn.send('HTTP/1.1 200 OK\n'.encode())
                    conn.send('Content-Type: text/html\n'.encode())
                    conn.send('Connection: close\n\n'.encode())
                    conn.sendall(self.__getResponse().encode())
                conn.close()
            except OSError as e:
                conn.close()
                print('Connection closed')
                
        wifi.stopAccessPoint()
