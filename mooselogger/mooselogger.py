import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def get_template_path(template_name):
    return os.path.join(os.path.dirname(__file__),'templates',template_name)        

class ContestLogListView(webapp.RequestHandler):
    def template_values_for_get(self):
        return {}

    def get(self):
        template_values = self.template_values_for_get()
        self.response.out.write(template.render(get_template_path('contest_log_list.html'), 
                                                template_values))

application = webapp.WSGIApplication(
                                     [('/', ContestLogListView)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

