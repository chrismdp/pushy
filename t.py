from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class PushHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write("HI")
		
def main():
	application = webapp.WSGIApplication([('push', PushHandler)], debug=True)
	run_wsgi_app(application)                                    

if __name__ == '__main__':
	main()
