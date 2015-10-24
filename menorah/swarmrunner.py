import os
import pprint
import json

# add logging to output errors to stdout
import logging
logging.basicConfig()

from nupic.swarming import permutations_runner


def _modelParamsToString(modelParams):
  pp = pprint.PrettyPrinter(indent=2)
  return pp.pformat(modelParams)



def _writeModelParamsToFile(modelParams, name):
  cleanName = name.replace(" ", "_").replace("-", "_")
  paramsName = "%s_model_params.py" % cleanName
  outDir = os.path.join(os.getcwd(), 'model_params')
  if not os.path.isdir(outDir):
    os.mkdir(outDir)
  outPath = os.path.join(os.getcwd(), 'model_params', paramsName)
  with open(outPath, "wb") as outFile:
    modelParamsString = _modelParamsToString(modelParams)
    outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
  return outPath



def _swarmForBestModelParams(swarmConfig, name, maxWorkers=4):
  outputLabel = name
  permWorkDir = os.path.abspath('swarm')
  if not os.path.exists(permWorkDir):
    os.mkdir(permWorkDir)
  modelParams = permutations_runner.runWithConfig(
    swarmConfig,
    {"maxWorkers": maxWorkers, "overwrite": True},
    outputLabel=outputLabel,
    outDir=permWorkDir,
    permWorkDir=permWorkDir,
    verbosity=0
  )
  modelParamsFile = _writeModelParamsToFile(modelParams, name)
  return modelParamsFile



def _printSwarmSizeWarning(size):
  if size.strip() == "small":
    print "= THIS IS A DEBUG SWARM. DON'T EXPECT YOUR MODEL RESULTS TO BE GOOD."
  elif size.strip() == "medium":
    print "= Medium swarm. Sit back and relax, this could take awhile."
  elif size.strip() == "large":
    print "= LARGE SWARM! Might as well load up the Star Wars Trilogy."
  else:
    raise Exception("Unknown swarm size \"%s\"", size)



def swarm(workingDir):
  name = os.path.splitext(os.path.basename(workingDir))[0]
  swarmDescriptionFile = os.path.join(workingDir, "swarm_description.json")
  with open(swarmDescriptionFile) as swarmDesc:
    swarmDescription = json.loads(swarmDesc.read())
  print "================================================="
  print "= Swarming on %s data..." % name
  _printSwarmSizeWarning(swarmDescription["swarmSize"])
  print "================================================="
  modelParams = _swarmForBestModelParams(swarmDescription, name)
  print "\nWrote the following model param files:"
  print "\t%s" % modelParams

