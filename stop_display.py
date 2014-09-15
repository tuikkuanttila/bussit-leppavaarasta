# -*- coding: utf-8 -*-
import cherrypy
import os
import json
import urllib
from jinja2 import Environment,FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
user = "tuikkuanttila"
passkey = "a7eyQrrio" 

class BusDisplay(object):
    
    def format_bus_number(self,original_string):
        num = original_string.split()[0]
        num = num[1:]
        return num
        
    def format_time(self,original_string):
        ostr = str(original_string)
        hours = ostr[0:2]
        mins = ostr[2:]
        return hours + ":" + mins

    @cherrypy.expose
    def leppavaara(self):
        name = "Leppävaara"
        departures = []
        
        urlbase = "http://api.reittiopas.fi/hsl/prod/?user=tuikkuanttila&pass=a7eyQrrio&request=stop&code="
        code = "2112261" # Kehä 1 länteen
        url = urlbase + code
        json_data = urllib.request.urlopen(url).read()
        data = json.loads(json_data.decode())
        departures_1w = data[0]["departures"]

        for d in departures_1w:
            d["code"] = self.format_bus_number(d["code"])
            d["time"] = self.format_time(d["time"])

        code = "2112262"
        url = urlbase + code
        json_data = urllib.request.urlopen(url).read()
        data = json.loads(json_data.decode())
        departures_1e = data[0]["departures"]

        for d in departures_1e:
            d["code"] = self.format_bus_number(d["code"])
            d["time"] = self.format_time(d["time"])
        
        template = env.get_template('leppavaara.html')
        return template.render(stop_name=name,departures_1w=departures_1w,departures_1e=departures_1e)
        
    
if __name__ == '__main__':

    conf =  {'/': {
                   'tools.staticdir.root': os.path.abspath(os.getcwd()) 
                },
            '/static': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir':os.path.join(os.path.abspath(os.getcwd()),"public")
              }
              }

    #cherrypy.server.socket_host = '192.168.0.147'
    #cherrypy.server.socket_port = 8080
    cherrypy.config.update({'server.socket_host':'0.0.0.0'})
    cherrypy.tree.mount(BusDisplay(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
