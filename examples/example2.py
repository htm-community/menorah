# This example grabs several streams from River View and swarms over all of them
# to predict energy demand, potentially using Airnow quality numbers to 
# contribute to predictions (I know this is dumb, but it is just an example).

from menorah import Menorah

sources =  [
  ["ercot-demand", "system_wide_demand", "Demand"],
  ["airnow", "Austin, TX", "Ozone"],
  ["airnow", "Beaumont-Port Arthur, TX", "Ozone"],
  ["airnow", "Brownsville-McAllen, TX", "Ozone"],
]

menorah = Menorah(sources, "work/example1-multifield")
menorah.swarm()
menorah.runModel(plot=True)
