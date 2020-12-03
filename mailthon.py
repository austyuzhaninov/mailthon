import os
import cherrypy
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import app_login, app_password


class Mailthon:

    @cherrypy.expose
    def index(self):
        return open('html/index.html').read()

    @cherrypy.expose
    def send(self, mail, msg):

        mm = MIMEMultipart()
        mm.attach(MIMEText(msg, 'plan'))

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()

        server.login(app_login, app_password)
        server.sendmail(app_login, mail, mm.as_string())
        server.quit()

        return Mailthon.index(self)


if __name__ == '__main__':

    if not os.path.exists('log'):
        os.mkdir('log')

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'engine.autoreload.on': False,
            'log.access_file': './log/access.log',
            'log.error_file': './log/error.log'
        }
    }

    cherrypy.quickstart(Mailthon(), '/', conf)
