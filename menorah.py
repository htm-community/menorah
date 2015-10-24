import csv
import json
import confluencefactory

from swarmtemplate import createSwarmDescription

class Menorah(object):


  def __init__(self, dataIds, since=None, limit=5000):
    self._streamIds = dataIds
    self._since = since
    self._limit = limit
    self._confluence = None


  def _createConfluence(self):
    self._confluence = confluencefactory.create(
      self._streamIds,
      since=self._since,
      limit=self._limit
    )


  def getStreamIds(self):
    return self._confluence.getStreamIds()


  def _createFieldDescription(self):
    return self._confluence.createFieldDescriptions()


  def writeCsv(self, path):
    self._createConfluence()
    with open(path, "w") as outputFile:
      writer = csv.writer(outputFile)
      headers = self.getStreamIds()
      fieldNames = ["timestamp"] + headers
      flags = ["T"] + ["" for h in headers]
      types = ["datetime"] + ["float" for h in headers]
      writer.writerow(fieldNames)
      writer.writerow(types)
      writer.writerow(flags)
      for row in self._confluence:
        writer.writerow(row)


  def writeSwarmDef(self, csvPath, outPath, predictedField):
    if self._confluence is None:
      raise Exception("Cannot write swarm description without first writing "
                      "input CSV.")
    fields = self._createFieldDescription()
    swarmDesc = createSwarmDescription(fields, csvPath, predictedField)
    with open(outPath, "w") as swarmOut:
      swarmOut.write(json.dumps(swarmDesc))


  def stream(self, handler):
    self._createConfluence()
    headers = ["datetime"] + self.getStreamIds()
    for row in self._confluence:
      handler(headers, row)
