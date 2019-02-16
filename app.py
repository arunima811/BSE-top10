import cherrypy
from jinja2 import Environment, FileSystemLoader
from mako.template import Template
import redis
import os, os.path
import ast
env = Environment(loader=FileSystemLoader('templates'))


cherrypy.config.update({'server.socket_port': 8090})

redisClient = redis.StrictRedis(
    host='localhost',
    port=6379,
    charset="utf-8",
    decode_responses=True)

table_dic = dict(redisClient.zrange("turnover_based_stocks", 0, 10, desc=True, withscores=True))
company_list = redisClient.hkeys("whole_data")
#print(company_list)
class Root:
    @cherrypy.expose
    def index(self, name = None):
        print(name)
        template = env.get_template("index.html")
        return template.render(data = table_dic, company_list= company_list)

@cherrypy.expose
class SearchService:
    @cherrypy.tools.accept(media='text/html')
    def POST(self, company):
        my_str = (redisClient.hget("whole_data", company))
        dic_str = ast.literal_eval(my_str)
        print(type(dic_str))
        template1 = env.get_template("company_stocks.html")
        return template1.render(name_of_company = company,company_details = dic_str)
        
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/search_company': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = Root()
    webapp.search_company = SearchService()
    cherrypy.quickstart(webapp, '/', conf)