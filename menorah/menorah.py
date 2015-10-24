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

import os
import errno
import csv
import json

import confluencefactory
from swarmtemplate import createSwarmDescription
from swarmrunner import swarm


# http://stackoverflow.com/a/600612/154560
def mkdirP(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: 
      raise


def createDir(path):
  if not os.path.isabs(path):
    myPath = path
  else:
    myPath = os.path.join(os.getcwd(), path)
  mkdirP(myPath)
  return myPath



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


  def writeSwarmDef(self, csvPath, outPath, 
                    predictedField=None, swarmParams=None):
    if self._confluence is None:
      raise Exception("Cannot write swarm description without first writing "
                      "input CSV.")
    if predictedField is None:
      predictedField = self.getStreamIds()[0]
    fields = self._createFieldDescription()
    swarmDesc = createSwarmDescription(
      fields, csvPath, predictedField, swarmParams=swarmParams
    )
    with open(outPath, "w") as swarmOut:
      swarmOut.write(json.dumps(swarmDesc))


  def prepareSwarm(self, path, predictedField=None, swarmParams=None):
    workingDir = createDir(path)
    csvPath = os.path.join(workingDir, "data.csv")
    self.writeCsv(csvPath)
    swarmDescriptionPath = os.path.join(workingDir, "swarm_description.json")
    self.writeSwarmDef(
      csvPath, swarmDescriptionPath, 
      predictedField=predictedField, swarmParams=swarmParams
    )


  def runSwarm(self, path):
    if not os.path.exists(path):
      raise Exception("Working directory %s does not exist!" % path)
    swarm(path)


  def swarm(self, path, predictedField=None, swarmParams=None):
    self.prepareSwarm(path, predictedField=predictedField, swarmParams=swarmParams)
    self.runSwarm(path)


  def stream(self, handler):
    self._createConfluence()
    headers = ["datetime"] + self.getStreamIds()
    for row in self._confluence:
      handler(headers, row)
