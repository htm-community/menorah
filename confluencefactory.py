from confluence import Confluence


def create(streamIds, since=None):
  confluence = Confluence(streamIds, since=since)
  confluence.load()
  return confluence


