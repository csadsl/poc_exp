from ConfigParser import ConfigParser
import os
from twisted.conch.error import ConchError
from twisted.internet import defer
from zope.interface.declarations import implements
from drupalorg.service import IServiceProtocol

__author__ = 'christophe'

class DummyServiceProtocol(object):
  implements(IServiceProtocol)

  def __init__(self, config, command):
    assert isinstance(config, ConfigParser)
    assert isinstance(command, str)

    self.command = command
    self.config = config

    self.deferred = None

  def request(self, *args):
    testFilePath = os.path.dirname(__file__) + "/testFiles/" + self.command

    filename = ""

    arguments = dict()
    for a in args:
      arguments.update(a)

    if len(arguments):
      if arguments.has_key('username'):
        filename += "_user-" + arguments['username']

      if arguments.has_key('password'):
        filename += "_pass-" + arguments['password']

      if arguments.has_key('fingerprint'):
        filename += "_fingerprint-" + arguments['fingerprint']

      if arguments.has_key('project_uri'):
        filename += "_project-" + arguments['project_uri']
    else:
      filename = "default"

    try:
      file = open(testFilePath + "/" + filename).read()
    except:
      self.deferred = defer.fail(NotImplementedError(testFilePath + "/" + filename))
    else:
      self.deferred = defer.succeed(file)


class DummyError(ConchError):
  pass
