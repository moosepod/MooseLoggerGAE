import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from models import ContactLog

def get_template_path(template_name):
    return os.path.join(os.path.dirname(__file__),'templates',template_name)        

class RequiresLogin(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.get_secured(user)

class ContestLogListView(RequiresLogin):
    def template_values_for_get(self,user):
        return {'logs': db.GqlQuery('SELECT * FROM ContactLog WHERE owner=:1 ORDER BY name',user).fetch(100) }

    def get_secured(self,user):
        template_values = self.template_values_for_get(user)
        self.response.out.write(template.render(get_template_path('contest_log_list.html'), 
                                                template_values))

application = webapp.WSGIApplication(
                                     [('/', ContestLogListView)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

