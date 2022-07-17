import wifi
import usocket as socket
import time
import re
import gc
from unquote import unquote_plus
from dnsquery import DNSQuery
gc.collect()


waitForConnectionTimeout = 10


class ConfigChanger:
    def __init__(self, config, display):
        self.config = config
        self.display = display
        self.waitForConnection = 0
        self.finished = False
        self.connectionSuccessful = False
        self.testBrightness=15

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
        with open("config_page.html") as config_page_file:
            config_page = config_page_file.read()
            config_page = re.sub('^\s*\{\s*$','{{', config_page)
            config_page = re.sub('^\s*\}\s*$','}}', config_page)
            return config_page.format(\
                connectionStatus={True: '<span style="color:green;">Connected</span>',\
                    False: '<span style="color:red;">Not connected</span>'}[self.connectionSuccessful],\
                ssid=self.config.getSsid(),\
                password=self.config.getPassword(),\
                plz=self.config.getPlz(),\
                brightness=self.config.getBrightness(),\
                brightnessNight=self.config.getBrightnessNight(),\
                timeNight=self.config.getTimeNight(),\
                testBrightness=self.testBrightness,\
                wifiList='<br>'.join(wifi.listNetworks())\
            )

    def __updateConfigFromRequest(self, request):
        containsQueryParameters = False
        changed = False
        testConnection = False
        print(request)
        if 'GET' in request:
            split1 = request.split('\n')[0].split(' ')[1].split('?')
            if len(split1) > 1:
                containsQueryParameters = True
                for paramValue in split1[1].split('&'):
                    if '=' in paramValue:
                        param, value = paramValue.split('=')
                        value = unquote_plus(value)
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
                    elif param == 'brightness' and value != self.config.getBrightness():
                        self.config.setBrightness(value)
                        changed = True
                    elif param == 'brightnessNight' and value != self.config.getBrightnessNight():
                        self.config.setBrightnessNight(value)
                        changed = True
                    elif param == 'timeNight' and value != self.config.getTimeNight():
                        self.config.setTimeNight(value)
                        changed = True
                    elif param == 'retest':
                        testConnection = True
                    elif param == 'testBrightness':
                        self.testBrightness = value
                        self.display.setBrightness(value)
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
        ip = wifi.startAccessPoint()
        self.__testWifiConnection()
        
        # dns server
        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.bind(('',53))
        
        # web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        s.listen(1)
        s.setblocking(False)

        while not self.finished:
            # DNS Loop
            try:
                data, addr = udps.recvfrom(1024)
                print("incomming dns datagram...")
                p=DNSQuery(data)
                udps.sendto(p.respuesta(ip), addr)
                print('Replying: {:s} -> {:s}'.format(p.dominio, ip))
            except OSError as e:
                pass
            
            # web loop
            try:
                conn = None
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
                if conn:
                    conn.close()
                
        wifi.stopAccessPoint()
