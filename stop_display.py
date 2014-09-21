# -*- coding: utf-8 -*-
import cherrypy
import os
import json
import urllib
from jinja2 import Environment,FileSystemLoader
from settings import user,passkey
env = Environment(loader=FileSystemLoader('templates'))

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

    def get_departures(self,urlbase,stop_code):
        url = urlbase + stop_code
        json_data = urllib.request.urlopen(url).read()
        data = json.loads(json_data.decode())
        departures = data[0]["departures"]
        
        if departures:
            for d in departures:
                d["code"] = self.format_bus_number(d["code"])
                d["time"] = self.format_time(d["time"])

        return departures
    
    @cherrypy.expose
    def leppavaara(self):
        name = "Leppävaara"
        departures = []
        
        urlbase = "http://api.reittiopas.fi/hsl/prod/?user=" + user + "&pass=" + passkey + "&request=stop&code="

        code = "2112261" # Kehä 1 länteen
        stops = []
        stop_1 = {}
        stop_1["departures"] = self.get_departures(urlbase,code)
        stop_1["stop_name"] = "Kehä 1 länteen (Otaniemen suunta)"
        stops.append(stop_1)
        
        code = "2112262"
        stop_2 = {}
        stop_2["departures"] = self.get_departures(urlbase,code)
        stop_2["stop_name"] = "Kehä 1 itään"
        stops.append(stop_2)

        code = "2111209"
        stop_3 = {}
        stop_3["departures"] = self.get_departures(urlbase,code)
        stop_3["stop_name"] = "Vanhaa Turuntietä Espoon suuntaan"
        stops.append(stop_3)

        code = "2111230"
        stop_4 = {}
        stop_4["departures"] = self.get_departures(urlbase,code)
        stop_4["stop_name"] = "Työmatkapysäkki"
        stops.append(stop_4)

        code = "2111222"
        stop_5 = {}
        stop_5["departures"] = self.get_departures(urlbase,code)
        stop_5["stop_name"] = "Karakallion suuntaan (20,26 ym)"
        stops.append(stop_5)

        code2 = "2111224"
        stop_5 = {}
        stop_5["departures"] = self.get_departures(urlbase,code2)
        stop_5["stop_name"] = "Karakallion suuntaan (24 ym)"
        stops.append(stop_5)

        template = env.get_template('leppavaara.html')
        return template.render(stops=stops)
        
    
if __name__ == '__main__':

    conf =  {'/': {
                   'tools.staticdir.root': os.path.abspath(os.getcwd()) 
                },
            '/static': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir':os.path.join(os.path.abspath(os.getcwd()),"public")
              }
              }

    cherrypy.config.update({'server.socket_host':'0.0.0.0'})
    cherrypy.tree.mount(BusDisplay(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
