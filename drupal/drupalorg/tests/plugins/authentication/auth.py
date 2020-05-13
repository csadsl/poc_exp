from twisted.plugin import IPlugin
from zope.interface.declarations import implements
from drupalorg import Session
from drupalorg.tests.plugins.authorization import auth
from gitexd.interfaces import IAuth

"""
    The following class copies the exact same behavior of DrupalAuth,
    the only difference is that it uses the DummyServiceProtocol.
"""

class DrupalTestAuth(auth.DrupalTestAuth):
  implements(IPlugin, IAuth)

  def authorizeRepository(self, user, repository, readOnly):
    """
          Whether or not the user may access the repository

          This should always return True in the case of Authentication tests.
    """

    return True

auth = DrupalTestAuth()
