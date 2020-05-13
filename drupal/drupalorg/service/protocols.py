from ConfigParser import ConfigParser
from twisted.conch.error import ConchError
from twisted.internet import reactor, defer
from twisted.internet.protocol import ProcessProtocol
from twisted.python import log
from twisted.web.client import getPage
from twisted.web.error import Error
import urllib, urlparse
from zope.interface import implements
from zope.interface.interface import Attribute, Interface

class IServiceProtocol(Interface):
  """Interface for Service objects to make requests."""

  dereferred = Attribute("Chain of actions that result in protocol invocation")

  def request(*args):
    """Setup a request for data.

Must use self.deferred for any asynchronous operations."""


class DrushError(ConchError):
  pass


class HTTPError(ConchError):
  pass


class DrushProcessProtocol(ProcessProtocol):
  implements(IServiceProtocol)

  DRUSH = "drush"

  """Read string values from Drush"""

  def __init__(self, config, command):
    assert isinstance(config, ConfigParser)
    assert isinstance(command, str)

    self.raw = str()
    self.raw_error = str()
    self.deferred = defer.Deferred()

    self.config = config
    self.command = command

  def outReceived(self, data):
    self.raw += data

  def errReceived(self, data):
    self.raw_error += data

  def outConnectionLost(self):
    self.result = self.raw.strip()

  def processEnded(self, status):
    if self.raw_error:
      log.err("Errors reported from drush:")
      for each in self.raw_error.split("\n"):
        log.err("  " + each)

    rc = status.value.exitCode

    if self.result and rc == 0:
      self.deferred.callback(self.result)
    else:
      if rc == 0:
        err = DrushError("Failed to read from drush.")
      else:
        err = DrushError("Drush failed ({0})".format(rc))

      self.deferred.errback(err)

  def request(self, *args):
    exec_args = [self.DRUSH,
                 "--root={0}".format(self.config.get("DEFAULT", "webRoot")),
                 self.command]
    for a in args:
      exec_args += a.values()

    reactor.spawnProcess(self, self.DRUSH, exec_args, env={"TERM": "dumb"})
    return self.deferred


class HTTPServiceProtocol(object):
  implements(IServiceProtocol)

  def __init__(self, config, url):
    assert isinstance(config, ConfigParser)
    assert isinstance(url, str)

    self.deferred = None

    self.command = url
    self.config = config

  def http_request_error(self, fail):
    fail.trap(Error)
    raise HTTPError("Could not open URL for {0}.".format(self.command))

  def request(self, *args):
    arguments = dict()
    for a in args:
      arguments.update(a)
    url_arguments = self.command + "?" + urllib.urlencode(arguments)
    constructed_url = urlparse.urljoin(self.config.get("DEFAULT", "serviceUrl"), url_arguments)
    self.deferred = getPage(constructed_url, headers=self.config.get("DEFAULT", "headers"))
    self.deferred.addErrback(self.http_request_error)