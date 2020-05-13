from drupalorg.tests.plugins import authorization
from drupalorg.tests.test_authentication import AuthenticationTests
from gitexd.interfaces import IAuth

__author__ = 'christophe'

class PushctlTests(AuthenticationTests):
  pluginPackages = {
    IAuth: authorization
  }

  def testPushEnabled(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "passAuth")

    def processEnded(result):
      self.assertNoError()
      self.assertEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)

  def testPushDisabled(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "passAuth-allPushesDisabled")

    def processEnded(result):
      self.assertError("Pushes to projects are currently disabled.")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)

  def testSandboxPushDisabled(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "passAuth-allSandboxPushesDisabled")

    def processEnded(result):
      self.assertError("Pushes to sandboxes are currently disabled.")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)

  def testSandboxPushEnabledCorePushDisabled(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "passAuth-sandboxPushEnabledCorePushDisabled")

    def processEnded(result):
      self.assertNoError()
      self.assertEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)


class AnonymousAuthorizationTests(AuthenticationTests):
  pluginPackages = {
    IAuth: authorization
  }

  def testAnonymousPull(self):
    self._setUp(allowAnon=True)

    remoteRepository = self._testHTTP()

    def processEnded(result):
      # Not equal because local repository has more commits than remote
      # there should have been no errors though
      self.assertNoError()
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pullRepository(self.repository).addCallback(processEnded)

  def testAnonymousPush(self):
    self._setUp(allowAnon=True)

    remoteRepository = self._testHTTP()

    def processEnded(result):
      self.assertError("You don't have access to this repository.")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository).addCallback(processEnded)


class AuthorizationTests(AuthenticationTests):
  pluginPackages = {
    IAuth: authorization
  }

  def testPasswordUserAuthorized(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "passAuth")

    def processEnded(result):
      self.assertNoError()
      self.assertEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)

  def testPasswordUserUnauthorized(self):
    self._setUp()

    remoteRepository = self._testSSH("john", "passAuth")

    def processEnded(result):
      self.assertError("User 'john' does not have write permissions for repository versioncontrol")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)

  def testDefaultUserAuthorized(self):
    self._setUp()

    remoteRepository = self._testSSH("git", "keyAuth")

    def processEnded(result):
      self.assertNoError()
      self.assertEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, keyFile="test").addCallback(processEnded)

  def testDefaultUserUnauthorized(self):
    self._setUp()

    remoteRepository = self._testSSH("git", "keyAuth_invalid")

    def processEnded(result):
      self.assertError("User 'None' does not have write permissions for repository versioncontrol")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, keyFile="test").addCallback(processEnded)

  def testKeyUserAuthorized(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "keyAuth")

    def processEnded(result):
      self.assertNoError()
      self.assertEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, keyFile="test").addCallback(processEnded)

  def testKeyUserUnauthorized(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "keyAuth_invalid")

    def processEnded(result):
      self.assertError("User 'test' does not have write permissions for repository versioncontrol")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, keyFile="test").addCallback(processEnded)

  def testDisabledProject(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "disabledProject")

    def processEnded(result):
      self.assertError("Project versioncontrol has been disabled")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)

  def testDisabledUser(self):
    self._setUp()

    remoteRepository = self._testSSH("test", "disabledUsers")

    def processEnded(result):
      self.assertError("You do not have permission to access 'versioncontrol' with the provided credentials.")
      self.assertNotEqual(self.repository, remoteRepository)

    return self.pushRepository(self.repository, "pass").addCallback(processEnded)
