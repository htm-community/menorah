import csv
import confluencefactory


class Menorah(object):


  def __init__(self, dataIds, since=None, limit=5000):
    self._streamIds = dataIds
    self._since = since
    self._limit = limit



  def writeCsv(self, path):
    confluence = confluencefactory.create(
      self._streamIds,
      since=self._since,
      limit=self._limit
    )
    with open(path, "w") as outputFile:
      writer = csv.writer(outputFile)
      headers = [":".join(header) for header in self._streamIds]
      writer.writerow(["datetime"] + headers)
      for row in confluence:
        writer.writerow(row)



  def stream(self, handler):
    confluence = confluencefactory.create(
      self._streamIds,
      since=self._since,
      limit=self._limit
    )
    headers = ["datetime"] + [":".join(header) for header in self._streamIds]
    for row in confluence:
      handler(headers, row)
