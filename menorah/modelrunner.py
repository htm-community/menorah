import importlib
import sys
import os
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

import nupic_output


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# _METRIC_SPECS = (
#     MetricSpec(field='', metric='multiStep',
#                inferenceElement='multiStepBestPredictions',
#                params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
#     MetricSpec(field='kw_energy_consumption', metric='trivial',
#                inferenceElement='prediction',
#                params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
#     MetricSpec(field='kw_energy_consumption', metric='multiStep',
#                inferenceElement='multiStepBestPredictions',
#                params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
#     MetricSpec(field='kw_energy_consumption', metric='trivial',
#                inferenceElement='prediction',
#                params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
# )

def _createModel(modelParams, predictedField):
  model = ModelFactory.create(modelParams)
  print predictedField
  model.enableInference({"predictedField": predictedField})
  return model



def _getModelParamsFromWorkDir(workingDir):
  modelParamsPath = os.path.join(workingDir, "model_params", "model_params.py")
  print "Importing model params from %s" % modelParamsPath
  myGlobals = {"MODEL_PARAMS": None}
  execfile(modelParamsPath, myGlobals)
  return myGlobals["MODEL_PARAMS"]



# def _runIoThroughNupic(inputData, fieldNames, predictedField, 
#                        model, workingDir, plot):
#   inputFile = open(inputData, "rb")
#   csvReader = csv.reader(inputFile)
#   # skip header rows
#   csvReader.next()
#   csvReader.next()
#   csvReader.next()
# 
#   shifter = InferenceShifter()
#   if plot:
#     output = nupic_output.NuPICPlotOutput([workingDir])
#   else:
#     output = nupic_output.NuPICFileOutput([workingDir])
# 
#   # metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
#   #                                 model.getInferenceType())
# 
#   counter = 0
#   for row in csvReader:
#     counter += 1
#     timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
#     rowDict = {
#       "timestamp": timestamp
#     }
#     for i, fieldName in enumerate(fieldNames):
#       rowDict[fieldName] = row[i + 1]
#     print row
#     print rowDict
#     result = model.run(rowDict)
#     
#     # result.metrics = metricsManager.update(result)
# 
#     if counter % 100 == 0:
#       print "Read %i lines..." % counter
#       # print ("After %i records, 1-step altMAPE=%f" % (counter,
#       #         result.metrics["multiStepBestPredictions:multiStep:"
#       #                        "errorMetric='altMAPE':steps=1:window=1000:"
#       #                        "field=%s" % predictedField]))
# 
#     if plot:
#       result = shifter.shift(result)
# 
#     prediction = result.inferences["multiStepBestPredictions"][1]
#     output.write([timestamp], [consumption], [prediction])
# 
#   inputFile.close()
#   output.close()



# def runModel(workingDirPath, fieldNames, predictedField, 
#              modelParams=None, plot=False):
#   if modelParams is None:
#     print "Creating model from %s..." % workingDirPath
#     modelParams = _getModelParamsFromName(workingDirPath)
# 
#   model = _createModel(modelParams)
#   inputData = os.path.join(workingDirPath, "data.csv")
#   _runIoThroughNupic(
#     inputData, fieldNames, predictedField, model, workingDirPath, plot
#   )


def createMetrics(predictedField):
  return (
      MetricSpec(field='', metric='multiStep',
                 inferenceElement='multiStepBestPredictions',
                 params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
      MetricSpec(field=predictedField, metric='trivial',
                 inferenceElement='prediction',
                 params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
      MetricSpec(field=predictedField, metric='multiStep',
                 inferenceElement='multiStepBestPredictions',
                 params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
      MetricSpec(field=predictedField, metric='trivial',
                 inferenceElement='prediction',
                 params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
  )


def getRowHandler(workingDirPath, predictedField, 
                  modelParams=None, plot=False):
  
  if modelParams is None:
    print "Creating model from %s..." % workingDirPath
    modelParams = _getModelParamsFromWorkDir(workingDirPath)
  else:
    print "Creating model from previously loaded model params."

  model = _createModel(modelParams, predictedField)
  
  # shifter = InferenceShifter()
  # if plot:
  #   output = nupic_output.NuPICPlotOutput([workingDirPath])
  # else:
  #   output = nupic_output.NuPICFileOutput([workingDirPath])
  
  metricsManager = MetricsManager(
    createMetrics(predictedField), 
    model.getFieldInfo(),
    model.getInferenceType()
  )
  
  global counter
  counter = 0
  
  def handler(headers, row):
    global counter
    dataDict = dict(zip(headers, row))
    result = model.run(dataDict)
    result.metrics = metricsManager.update(result)
    if counter % 100 == 0:
      print "Read %i lines..." % counter
      print ("After %i records, 1-step altMAPE=%f" % (counter,
              result.metrics["multiStepBestPredictions:multiStep:"
                             "errorMetric='altMAPE':steps=1:window=1000:"
                             "field=%s" % predictedField]))

    counter += 1
    
    # TODO: process output.
    # if plot:
    #   result = shifter.shift(result)
    # 
    # prediction = result.inferences["multiStepBestPredictions"][1]
    # output.write([timestamp], [consumption], [prediction])

  return handler