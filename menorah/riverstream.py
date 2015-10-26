# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the MIT License along with this 
# program.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from datetime import datetime


DEFAULT_LAST_VALUE = 0
TIMESTAMP_FIELD = "datetime"


class RiverStream(object):

  
  def __init__(self, client, dataId, since=None, until=None, limit=5000):
    riverName = dataId[0]
    streamName = dataId[1]
    self._id = dataId
    self._client = client
    self._stream = self._client.river(riverName).stream(streamName)
    if dataId[2].startswith("aggregate="):
      self._aggregate = dataId[2].split("=").pop()
      self._field = "count"
    else:
      self._aggregate = None
      self._field = dataId[2]
    self._dataHandle = None
    self._data = []
    self._headers = []
    # The cursor is the position for the next value.
    self._cursor = 0
    self._since = since
    self._until = until
    self._limit = limit
    self._lastValue = DEFAULT_LAST_VALUE
    self._min = None
    self._max = None
    self._dataType = "float"


  def __len__(self):
    return len(self._data) - self._cursor


  def _fetchNextData(self):
    print "Loading next data cursor for %s..." % self.getName()
    self._dataHandle = self._dataHandle.next()
    self._cursor = 0
    self._data = self._dataHandle.data()
    self._headers = self._dataHandle.headers()
    print "Loaded %i rows." % len(self)


  def _updateMinMax(self, value):
    min = self._min
    max = self._max
    if min is None or value < min:
      self._min = value
    if max is None or value > max:
      self._max = value


  def load(self):
    """
    Loads this stream by calling River View for data.
    """
    print "Loading data for %s..." % self.getName()
    self._dataHandle = self._stream.data(
      since=self._since, until=self._until, 
      limit=self._limit, aggregate=self._aggregate
    )
    self._data = self._dataHandle.data()
    self._headers = self._dataHandle.headers()
    print "Loaded %i rows." % len(self)


  def next(self):
    """
    Returns the next data value.
    :return: (float|int) the next data value
    """
    out = self.peek()[self._headers.index(self._field)]
    self._cursor += 1
    if out is not None:
      self._lastValue = out
    return out


  def last(self):
    """
    Returns the data value before the one coming next.
    :return: (float|int) last data value
    """
    return self._lastValue


  def peek(self):
    """
    Returns the next data value without advancing.
    :return: (float|int) last next value
    """
    if len(self) is 0:
      raise Exception("RiverStream object is empty!")
    return self._data[self._cursor]


  def advance(self, myDateTime):
    """
    Advances to the next value and returns an appropriate value for the given
    time.
    :param myDateTime: (datetime) when to fetch the value for 
    :return: (float|int) value for given time
    """
    if self.getTime() == myDateTime:
      out =  self.next()
      # Sometimes, the stream has no value for this field and returns None, in 
      # this case we'll use the last value as well.
      if out is None:
        out = self.last()
    else:
      out = self.last()
    # If there's no more data, we must fetch more
    if len(self) is 0:
      self._fetchNextData()
    
    self._updateMinMax(out)
    
    if isinstance(out, float):
      self._dataType = "float"
    
    # Convert to proper data type
    if self._dataType is "float":
      out = float(out)
    else:
      out = int(out)

    return out


  def reset(self):
    self.load()
    self._cursor = 0


  def getName(self):
    """
    Gets the id for this stream.
    :return: (string)
    """
    return " ".join(self._id)


  def getTime(self):
    """
    Gets the time for the next data point.
    :return: (datetime)
    """
    headers = self._headers
    timeStringIndex = headers.index(TIMESTAMP_FIELD)
    timeString = self.peek()[timeStringIndex]
    return  datetime.strptime(timeString, "%Y/%m/%d %H:%M:%S")


  def createFieldDescription(self):
    """
    Provides a field description dict for swarm description.
    :return: (dict)
    """
    return {
      "fieldName": self.getName(),
      "fieldType": self._dataType,
      "minValue": self._min,
      "maxValue": self._max
    }


  def getDataType(self):
    return self._dataType


  def __str__(self):
    return self.getName()