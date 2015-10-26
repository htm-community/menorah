# In an attempt to better predict the number of "tree debris" 311 calls in 
# Chicago, this experiment incorporates data from local weather stations.

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
