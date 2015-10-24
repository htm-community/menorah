import os
import copy


SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "timestamp",
      "fieldType": "datetime"
    },
  ],
  "streamDef": {
    "info": "kw_energy_consumption",
    "version": 1,
    "streams": [
      {
        "info": "",
        "source": "file://",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": ""
  },
  "iterationCount": 3000,
  "swarmSize": "medium"
}

FIELD = {
  "fieldName": "",
  "fieldType": "float",
  "maxValue": None,
  "minValue": None
}

def createSwarmDescription(fields, csvPath, predictedField, swarmParams=None):
  swarmDesc = copy.deepcopy(SWARM_DESCRIPTION)
  swarmDesc["includedFields"] = swarmDesc["includedFields"] + fields
  swarmDesc["inferenceArgs"]["predictedField"] = predictedField
  outStream = swarmDesc["streamDef"]["streams"][0]
  outStream["info"] = csvPath
  outStream["source"] = outStream["source"] + os.path.abspath(csvPath)
  if swarmParams is not None:
    swarmDesc.update(swarmParams)
  return swarmDesc