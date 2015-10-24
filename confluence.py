from riverpy import RiverViewClient

from riverstream import RiverStream

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class Confluence(object):


  def __init__(self, dataIds, since=None, until=None, limit=None):
    self._dataIds = dataIds
    self._since = since
    self._until = until
    self._limit = limit
    self._streams = []


  def __iter__(self):
    return self


  def _createStreams(self):
    client = RiverViewClient(debug=False)
    for dataId in self._dataIds:
      self._streams.append(
        RiverStream(
          client, dataId, 
          since=self._since, 
          until=self._until, 
          limit=self._limit
        )
      )


  def _loadData(self):
    [stream.load() for stream in self._streams]


  def load(self):
    self._createStreams()
    self._loadData()


  def next(self):
    if self._isEmpty():
      raise StopIteration
    
    # Peek at next item in each data stream and pick the earliest value to lead
    # the next row of data
    earliest = min([stream.getTime() for stream in self._streams])
    timeString = earliest.strftime(DATE_FORMAT)
    rowData = [stream.advance(earliest) for stream in self._streams]
    out = [timeString] + rowData
    return out


  def _isEmpty(self):
    smallest = min([len(stream) for stream in self._streams])
    return smallest is 0


  def createFieldDescriptions(self):
    return [stream.createFieldDescription() for stream in self._streams]


  def getStreamIds(self):
    return [str(stream) for stream in self._streams]