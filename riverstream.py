from datetime import datetime

from riverpy import RiverViewClient


class RiverStream(object):

  
  def __init__(self, dataId):
    riverName = dataId[0]
    streamName = dataId[1]
    self._client = RiverViewClient(debug=True)
    self._stream = self._client.river(riverName).stream(streamName)
    self._cursor = None


  def load(self):
    self._cursor = self._stream.data()


  def isMaxedOut(self):
    return len(self._cursor.data()) >= 5000


  def getTime(self):
    # TODO: fail if empty
    timestamp = self._cursor.data()[0]["datetime"]
    return datetime.fromtimestamp(timestamp)
