from gitexd.tests import _createDefaultConfigFile

def _createDrupalAuthConfigFile(repoPath='', allowAnon=False):
  defaults = {
    "allowAnonymous": allowAnon,
    "authServiceProtocol": "dummy"
  }

  return _createDefaultConfigFile(repoPath, defaults)