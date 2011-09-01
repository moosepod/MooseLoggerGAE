from google.appengine.ext import db
from google.appengine.api import users

class Ruleset(db.Model):
  """ Set of rules governing scoring/validation of the entries in a log """
  name = db.StringProperty(multiline=False)

class ContactLog(db.Model):
  """ Represents a set of log entries for a given user. """
  owner = db.UserProperty()
  name = db.StringProperty(multiline=False)
  ruleset = db.ReferenceProperty(reference_class=Ruleset)
  when_created = db.DateTimeProperty(auto_now_add=True)


