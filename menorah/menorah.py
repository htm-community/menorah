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
import modelrunner


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


def banner(text, ch="*", length=82):
  spaced_text = " %s " % text
  print("\n" + spaced_text.center(length, ch) + "\n")



class Menorah(object):


  def __init__(self, dataIds, workingDir, since=None, limit=5000, debug=False):
    """
    Creates a new Menorah instance.
    :param dataIds: (list) Each data id in this list is a list of strings:
                    1. river name
                    2. stream name
                    3. field name
    :param workingDir: path to store NuPIC artifacts
    :param since: (datetime) when to start the data fetch
    :param limit: (int) how many rows of data to get initially
    """
    self._streamIds = dataIds
    self._workingDir = workingDir
    self._since = since
    self._limit = limit
    self._confluence = None
    self._modelParams = None
    self._predictedField = None
    self._debug = debug


  def _createConfluence(self):
    if self._confluence is not None: 
      return
    self._confluence = confluencefactory.create(
      self._streamIds,
      since=self._since,
      limit=self._limit,
      debug=self._debug
    )
    self._predictedField = self.getStreamIds()[0]


  def _createFieldDescription(self):
    return self._confluence.createFieldDescriptions()


  def getStreamIds(self):
    """
    Gets all the stream ids that Menorah was created with.
    :return: list of stream id strings
    """
    return self._confluence.getStreamIds()


  def resetConfluence(self):
    if self._confluence is None:
      self._createConfluence()
    self._confluence.resetStreams()


  def populateCsv(self):
    """
    Writes data from streams into CSV in working directory.
    :return:
    """
    workingDirPath = createDir(self._workingDir)
    csvPath = os.path.join(workingDirPath, "data.csv")
    self.writeCsv(csvPath)
    return csvPath, workingDirPath


  def writeCsv(self, path):
    """
    Writes data one or many streams into one CSV file.
    :param path: absolute or relative file path
    """
    self._createConfluence()
    with open(path, "w") as outputFile:
      writer = csv.writer(outputFile)
      headers = self.getStreamIds()
      fieldNames = ["timestamp"] + headers
      flags = ["T"] + ["" for h in headers]
      types = ["datetime"] + self._confluence.getDataTypes()
      writer.writerow(fieldNames)
      writer.writerow(types)
      writer.writerow(flags)
      for row in self._confluence:
        writer.writerow(row)
    print "Wrote CSV data to %s." % path


  def writeSwarmDescription(self, csvPath, outPath, 
                    predictedField=None, swarmParams=None):
    """
    Writes swarm description file (JSON).
    :param csvPath: path to CSV data
    :param outPath: absolute or relative file path to write swarm JSON file 
    :param predictedField: (string)
    :param swarmParams: (dict) overrides any swarm params
    """
    if self._confluence is None:
      raise Exception("Missing Confluence! Cannot attempt operation requiring "
                      "data without first loading the data.")
    if predictedField is None:
      predictedField = self._predictedField
    fields = self._createFieldDescription()
    swarmDesc = createSwarmDescription(
      fields, csvPath, predictedField, swarmParams=swarmParams
    )
    with open(outPath, "w") as swarmOut:
      swarmOut.write(json.dumps(swarmDesc))


  def prepareSwarm(self, predictedField=None, swarmParams=None):
    """
    Gathers data from streams into local CSV file, then creates a swarm 
    description for it. 
    :param predictedField: (string)
    :param swarmParams: (dict) overrides any swarm params
    """
    csvPath, workingDirPath = self.populateCsv()
    swarmDescriptionPath = os.path.join(
      workingDirPath, "swarm_description.json"
    )
    self.writeSwarmDescription(
      csvPath, swarmDescriptionPath, 
      predictedField=predictedField, swarmParams=swarmParams
    )


  def runSwarm(self, workingDirPath):
    """
    Runs a swarm with data within a working directory. This assumes that the 
    user has already run prepareSwarm().
    :param workingDirPath: absolute or relative path to working directory
    """
    if not os.path.exists(workingDirPath):
      raise Exception("Working directory %s does not exist!" % workingDirPath)
    banner("RUNNING SWARM")
    self._modelParams = swarm(workingDirPath)


  def swarm(self, predictedField=None, swarmParams=None):
    """
    Runs a swarm on data and swarm description found within the given working
    directory. 
    
    If no predictedField is provided, it is assumed that the first stream listed
    in the streamIds provided to the Menorah constructor is the predicted field.
    
    :param predictedField: (string)
    :param swarmParams: (dict) overrides any swarm params
    :return:
    """
    self.prepareSwarm(
      predictedField=predictedField, swarmParams=swarmParams
    )
    self.runSwarm(self._workingDir)


  def runModel(self, plot=False):
    self.resetConfluence()
    (handler, whenDone) = modelrunner.getRowHandlers(
      self._workingDir, 
      self._predictedField, 
      modelParams=self._modelParams, 
      plot=plot
    )
    banner("RUNNING MODEL")
    self.stream(handler, whenDone)


  def stream(self, handler, whenDone=None):
    """
    Fetches data from river streams and feeds them into the given function.
    :param handler: (function) passed headers [list] and row [list] of the data
                    for one time step, for every row of data
    """
    self._createConfluence()
    headers = ["timestamp"] + self.getStreamIds()
    for row in self._confluence:
      handler(headers, row)
    
    if whenDone is not None:
      whenDone()
