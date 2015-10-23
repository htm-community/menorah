import csv
import confluencefactory


class Menorah(object):


  def __init__(self, dataIds, since=None):
    self._streamIds = dataIds
    self._since = since



  def writeCsv(self, path):
    confluence = confluencefactory.create(
      self._streamIds,
      since=self._since
    )
    with open(path, "w") as outputFile:
      while confluence is not None:
        writer = csv.writer(outputFile)
        row = confluence.nextRow()
        writer.writerow(row)



  def stream(self, handler):
    pass