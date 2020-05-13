from twisted.internet.defer import DeferredList
from twisted.python.failure import Failure
from zope.interface.declarations import implements
from zope.interface.interface import Interface
from gitexd import Factory
from gitexd.protocol import PULL, PUSH
from gitexd.protocol.error import GitError
from gitexd.interfaces import IException

class DrupalOrgAuthException(GitError):
  implements(IException)

  def __init__(self, message, proto=None):
    GitError.__init__(self, message, proto)


def getProjectName(repository):
  parts = repository.split('/')

  for part in parts:
    if len(part) > 4 and part[-4:] == '.git':
      return part[:-4]

  return None


def _mapUser(users, username, password, fingerprint):
  assert isinstance(users, dict)
  assert username is None or isinstance(username, str)
  assert fingerprint is None or isinstance(fingerprint, str)

  if username is None and fingerprint is not None:
    for user in users.values():
      if fingerprint in user["ssh_keys"].values():
        return user
  elif username is not None and username in users:
    user = users[username]

    # Next block might seem pointless, but before the new hashing method was introduced here we did
    # an additional (but redundant) check on the authentication stuff.
    # The returned hash in the authData seems to be a substring of the one calculated by drupalpass,
    # but let's just comment it out for a while.
    if fingerprint in user["ssh_keys"].values():
      return user
    #elif password == user["pass"]:
    #  return user
    else:
      return user
  else:
    return None


class ISession(Interface):
  """ """

  def mayAccess(self, app, repository, requestType):
    """Whether or not the current session may access a certain repository"""

  def __str__():
    """Should return name of committer in a string representation. Used for mapping committer to mnemomic id."""


class Session(object):
  implements(ISession)

  def __init__(self, app, authService, pushctlService, data):
    assert isinstance(app, Factory)
    assert isinstance(data, dict)

    self._app = app

    self._username = data["username"] if data.has_key("username") else None
    self._password = data["password"] if data.has_key("password") else None
    self._fingerprint = data["fingerprint"] if data.has_key("fingerprint") else None

    self._authService = authService
    self._pushctlService = pushctlService

  def mayAccess(self, repository, requestType):
    def _authCallback(data):
      auth, pushctl = data
      auth, authData = auth
      pushctl, pushctlData = pushctl

      if isinstance(authData, Failure):
        return authData
      elif isinstance(pushctlData, Failure):
        return pushctlData

      if not auth or not isinstance(authData, dict):
        return Failure(DrupalOrgAuthException("Repository does not exist. Verify that your remote is correct."))
      elif not isinstance(pushctlData, int):
        return Failure(DrupalOrgAuthException("Drupal.org is having some troubles."))
      elif auth and pushctl and requestType == PUSH:
        mask = authData["repo_group"] & pushctlData

        if mask:
          error = "Pushes for this type of repository are currently disabled."

          if mask & 0x01:
            error = "Pushes to core are currently disabled."
          if mask & 0x02:
            error = "Pushes to projects are currently disabled."
          if mask & 0x04:
            error = "Pushes to sandboxes are currently disabled."

          return Failure(DrupalOrgAuthException(error))

        else:
          if not authData["status"]:
            return Failure(DrupalOrgAuthException("Project {0} has been disabled".format(authData['repository_name'])))

          user = _mapUser(authData["users"], self._username, self._password, self._fingerprint)

          if user is None:
            return Failure(DrupalOrgAuthException(
              "User '{1}' does not have write permissions for repository {0}".format(authData['repository_name'],
                                                                                     self._username)))
          elif not user["global"]:
            return True
          else:
            # Account is globally disabled or disallowed
            # 0x01 = no Git user role, but unknown reason (probably a bug!)
            # 0x02 = Git account suspended
            # 0x04 = Git ToS unchecked
            # 0x08 = Drupal.org account blocked
            error = []

            if user["global"] & 0x02:
              error.append("Your Git access has been suspended.")
            if user["global"] & 0x04:
              error.append("You are required to accept the Git Access Agreement in your user profile before using Git.")
            if user["global"] & 0x08:
              error.append("Your Drupal.org account has been blocked.")

            if len(error) == 0:
              if user["global"] == 0x01:
                error.append("You do not have permission to access '{0}' with the provided credentials.\n".format(
                  authData['repository_name']))
              else:
                error.append(
                  "This operation cannot be completed at this time.  It may be that we are experiencing technical difficulties or are currently undergoing maintenance.")

            return Failure(DrupalOrgAuthException("\n".join(error)))
      else:
        # All repositories are publicly readable.
        return True

    project = getProjectName(repository)

    if project is None:
      return False

    self._authService.request_json({
      "project_uri": project
    })

    # Adding project_uri as an argument for push-control is not required
    # but is handy for testing purposes.
    self._pushctlService.request_json({
      "project_uri": project
    })

    d = DeferredList([self._authService.deferred, self._pushctlService.deferred], consumeErrors=True)
    d.addCallback(_authCallback)

    return d

  def __str__(self):
    if self._username is not None:
      return self._username
    else:
      return "anonymous"


class AnonymousSession(object):
  implements(ISession)

  def __init__(self, app, service):
    self._app = app
    self._service = service

  def mayAccess(self, repository, requestType):
    return requestType == PULL

  def __str__(self):
    return "anonymous"
