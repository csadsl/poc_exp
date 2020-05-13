import json
from drupalorg.service.protocols import IServiceProtocol

class Service(object):
  """Wrapper class for requests out to external services.
Protocol doesn't have to be a real protocol, but must conform to the interface specified by IServiceProtocol."""

  bool_map = {"true": True, "false": False} # PHP booleans - add more if needed

  def __init__(self, protocol):
    assert IServiceProtocol.providedBy(protocol)

    self.protocol = protocol

  def convert_bool(self, raw):
    result = self.bool_map[raw.strip()]
    return result

  def request_bool(self, *args):
    self.protocol.request(*args)
    self.protocol.deferred.addCallback(self.convert_bool)

  def convert_json(self, raw):
    try:
      result = json.loads(raw)
      return result
    except ValueError:
      print ("Protocol {0}:{1} returned bad JSON.".format(self.protocol.__class__, self.protocol.command))

  def request_json(self, *args):
    self.protocol.request(*args)
    self.protocol.deferred.addCallback(self.convert_json)

  def addCallback(self, *args):
    self.protocol.deferred.addCallback(*args)

  def addErrback(self, *args):
    self.protocol.deferred.addErrback(*args)

  @property
  def deferred(self):
    return self.protocol.deferred
