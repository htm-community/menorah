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


def touch(fname, times=None):
  with open(fname, 'a'):
    os.utime(fname, times)


def _writeModelParamsToFile(modelParams, workingDir):
  paramsName = "model_params.py"
  outDir = os.path.join(workingDir, 'model_params')
  if not os.path.isdir(outDir):
    os.mkdir(outDir)
  outPath = os.path.join(workingDir, 'model_params', paramsName)
  with open(outPath, "wb") as outFile:
    modelParamsString = _modelParamsToString(modelParams)
    outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
  touch(os.path.join(outDir, "__init__.py"))
  return outPath



def _swarmForBestModelParams(swarmConfig, name, workingDir, maxWorkers=8):
  outputLabel = name
  permWorkDir = os.path.join(workingDir, "swarm")
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
  _writeModelParamsToFile(modelParams, workingDir)
  return modelParams



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
  """
  Runs a swarm in the giving working directory, assuming it was created by 
  Menorah.
  :param workingDir: absolute or relative path to working directory created by
                     Menorah
  """
  name = os.path.splitext(os.path.basename(workingDir))[0]
  swarmDescriptionFile = os.path.join(workingDir, "swarm_description.json")
  with open(swarmDescriptionFile) as swarmDesc:
    swarmDescription = json.loads(swarmDesc.read())
  print "================================================="
  print "= Swarming on %s data..." % name
  _printSwarmSizeWarning(swarmDescription["swarmSize"])
  print "================================================="
  modelParams = _swarmForBestModelParams(swarmDescription, name, workingDir)
  return modelParams

