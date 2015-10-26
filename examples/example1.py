# This example shows how to stream River View data into a NuPIC swarm in an 
# attempt to prediction energy consumption in Texas. Once the swarm is complete,
# the resulting model parameters are used for running the data once again 
# through a newly created NuPIC model.

from menorah import Menorah

dataIds =  [
  # http://data.numenta.org/ercot-demand/system_wide_demand/data.html
  ["ercot-demand", "system_wide_demand", "Demand"],
]

menorah = Menorah(dataIds, "work/example1-one-field")
menorah.swarm()
menorah.runModel()

# Find your predictions in "work/one-field/predictions.csv"

