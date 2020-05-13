from twisted.plugin import IPlugin
from zope.interface.declarations import implements
from drupalorg.plugins.auth import DrupalAuth
from drupalorg.tests.plugins import DummyServiceProtocol
from gitexd.interfaces import IAuth

"""
    The following class copies the exact same behavior of DrupalAuth,
    the only difference is that it uses the DummyServiceProtocol.
"""

class DrupalTestAuth(DrupalAuth):
  implements(IPlugin, IAuth)

  def __init__(self):
    self.protocol = DummyServiceProtocol

auth = DrupalTestAuth()
