# This example grabs several streams from River View and swarms over all of them
# to predict energy demand, potentially using Airnow quality numbers to 
# contribute to predictions (I know this is dumb, but it is just an example).

from datetime import datetime

from menorah import Menorah

sources =  [
  ["chicago-311", "Tree Debris", "aggregate=1 day"],
  ["chicago-beach-weather", "Foster Weather Station", "humidity"],
  ["chicago-beach-weather", "Foster Weather Station", "interval_rain"],
  ["chicago-beach-water-quality", "Osterman Beach", "wave_height"],
]

menorah = Menorah(
  sources,
  "work/example5-multifield-aggregated", 
  since=datetime(2015, 5, 20)
)

menorah.swarm()
menorah.runModel(plot=True)
