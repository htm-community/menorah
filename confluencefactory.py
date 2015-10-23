from confluence import Confluence


def create(streamIds, **kwargs):
  print "Creating Confluence for %s" % ", ".join([":".join(row) for row in streamIds])
  confluence = Confluence(streamIds, **kwargs)
  confluence.load()
  return confluence


