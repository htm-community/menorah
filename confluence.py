from riverstream import RiverStream

class Confluence(object):


  def __init__(self, dataIds, since=None, until=None):
    self._dataIds = dataIds
    self._since = since
    self._until = until
    self._streams = []


  def _createStreams(self):
    for dataId in self._dataIds:
      self._streams.append(RiverStream(dataId))


  def _loadData(self):
    for stream in self._streams:
      stream.load()


  def _alignStreams(self):
    # If any streams are maxed out, chop off all other data cursors at the
    # same "until" time so they are all aligned
    maxedOut = [stream.isMaxedOut() for stream in self._streams]
    
    # Adjust the "until" time property on this instance to reflect the new 
    # state.
    
    pass


  def load(self):
    self._createStreams()
    self._loadData()
    self._alignStreams()


  def _loadNext(self):
    # Get new data cursor for each stream one time step into the future.
    pass


  def nextRow(self):
    if self.isEmpty():
      self._loadNext()
    
    # Peek at next item in each data stream and pick the earliest value to lead
    # the next row of data
    times = [stream.getTime() for stream in self._streams]
    
    # Create output row with dummy values for missing data and return.


  def isEmpty(self):
    pass
