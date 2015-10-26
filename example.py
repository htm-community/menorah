from menorah import Menorah

dataIds =  [
  # http://data.numenta.org/ercot-demand/system_wide_demand/data.html
  ["ercot-demand", "system_wide_demand", "Demand"],
]

menorah = Menorah(dataIds, "work/one-field")
menorah.swarm()
menorah.runModel()

# Find your predictions in "work/one-field/predictions.csv"

