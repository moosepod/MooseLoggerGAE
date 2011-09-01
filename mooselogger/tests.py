import unittest
import StringIO

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed

from models import Ruleset, ContactLog
from mooselogger import ContestLogListView

class ViewTests(unittest.TestCase):
    class MockResponse(object):
        def __init__(self):
            self.out = StringIO.StringIO()

        def __unicode__(self):
            return self.out.getvalue()

    class MockRequest(object):
        def __init__(self):
            self.uri = '/test'

    def test_contact_log_list(self):
        user = users.User(email='foo@bar.com')
        view = ContestLogListView()
        view.response = ViewTests.MockResponse()
        view.request = ViewTests.MockRequest()

        self.assertEquals({'logs': []}, view.template_values_for_get(user))
        self.assertEquals(u'', unicode(view.response))

        view.get_secured(user)  
        self.assertTrue('<h1>Your Logs</h1>' in  unicode(view.response))

        view.get()

class ModelSanityTests(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
	
    # Create a consistency policy that will simulate the High Replication consistency model.
    self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
    # Initialize the datastore stub with this policy.
    self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

  def test_ruleset(self):
    rs = Ruleset(name='Foo Bar')
    rs.put()

    rs2 = db.get(rs.key())
    self.assertEquals(rs.name, rs2.name)

  def test_contactlog(self):
    user = users.User(email='foo@bar.com')

    rs = Ruleset(name='Foo Bar')
    rs.put()

    cl = ContactLog(name='Quux', ruleset=rs, owner=user)
    cl.put()

    cl2 = db.get(cl.key())
    self.assertEquals('Quux', cl.name)
    self.assertEquals(rs, cl.ruleset)
    self.assertEquals(user, cl.owner)
    self.assertTrue(cl.when_created)
 
