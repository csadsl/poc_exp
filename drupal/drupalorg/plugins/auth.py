from twisted.conch.ssh.keys import Key
from twisted.cred.credentials import ISSHPrivateKey, IUsernamePassword
from twisted.internet import defer
from twisted.plugin import IPlugin
from zope.interface.declarations import implements
from drupalorg.drupalpass import DrupalHash
from drupalorg import ISession, AnonymousSession, Session
from drupalorg.service import IServiceProtocol, Service
from drupalorg.service.protocols import HTTPServiceProtocol
from gitexd import Factory
from gitexd.interfaces import IAuth
from gitexd.protocol import PUSH, PULL

class DrupalAuth(object):
  implements(IPlugin, IAuth)

  SessionInterface = ISession

  def __init__(self):
    self.protocol = HTTPServiceProtocol

  def _handleProtocolCallback(self, result, app, data):
    assert isinstance(app, Factory)
    assert isinstance(data, dict)

    if result:
      authService = Service(self.protocol(app.getConfig(), 'vcs-auth-data'))
      pushctlService = Service(self.protocol(app.getConfig(), 'pushctl-state'))

      return Session(app, authService, pushctlService, data)
    else:
      return None

  def allowAnonymousAccess(self, app):
    assert isinstance(app, Factory)

    if app.getConfig().get("DEFAULT", "allowAnonymous", True):
      service = Service(self.protocol(app.getConfig(), 'vcs-auth-data'))

      return defer.succeed(AnonymousSession(app, service))
    else:
      return defer.succeed(None)

  def authenticateKey(self, app, credentials):
    assert isinstance(app, Factory)
    assert ISSHPrivateKey.providedBy(credentials)

    key = Key.fromString(credentials.blob)
    fingerprint = key.fingerprint().replace(':', '')

    service = None
    data = {}

    if credentials.username == "git":
      service = Service(self.protocol(app.getConfig(), 'drupalorg-sshkey-check'))

      data = {
        "fingerprint": fingerprint
      }

      service.request_bool(data)
    else:
      service = Service(self.protocol(app.getConfig(), 'drupalorg-ssh-user-key'))

      data = {
        "username": credentials.username,
        "fingerprint": fingerprint
      }

      service.request_bool(data)

    service.addCallback(self._handleProtocolCallback, app, data)

    return service.deferred

  def authenticatePassword(self, app, credentials):
    assert isinstance(app, Factory)
    assert IUsernamePassword.providedBy(credentials)

    service = Service(self.protocol(app.getConfig(), 'drupalorg-vcs-auth-fetch-user-hash'))
    service.request_json({"username": credentials.username})

    def _authCallback(result):
      if result:
        service = Service(self.protocol(app.getConfig(), 'drupalorg-vcs-auth-check-user-pass'))

        data = {
          "username": credentials.username,
          "password": DrupalHash(result, credentials.password).get_hash()
        }

        service.request_bool(data)

        service.addCallback(self._handleProtocolCallback, app, data)

        return service.deferred
      else:
        return None

    service.addCallback(_authCallback)

    return service.deferred

  def authorizeRepository(self, session, repository, requestType):
    assert ISession.providedBy(session)
    assert requestType in (PULL, PUSH)

    return session.mayAccess(repository, requestType)

  def authorizeReferences(self, session, refs, requestType):
    return True

  def _invariant(self):
    assert IServiceProtocol.implementedBy(self._protocol)

auth = DrupalAuth()
