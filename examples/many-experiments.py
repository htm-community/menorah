# This file runs a series of experiments that includes swarming, so it will 
# take a long time to run. This might be an overnight job. Each instance of 
# Menorah writes to a different working directory so that the swarm results are
# retained and models can be run against them later. 

from datetime import datetime

from menorah import Menorah

# Tree Debris vs weather.

sources =  [
  ["chicago-311", "Tree Debris", "aggregate=1 day"],
  ["chicago-beach-weather", "Foster Weather Station", "humidity"],
  ["chicago-beach-weather", "Foster Weather Station", "interval_rain"],
  ["chicago-beach-weather", "Foster Weather Station", "barometric_pressure"],
  ["chicago-beach-weather", "Foster Weather Station", "wind_speed"],
  ["chicago-beach-weather", "Foster Weather Station", "maximum_wind_speed"],
  ["chicago-beach-weather", "Foster Weather Station", "air_temperature"],
  ["chicago-beach-water-quality", "Osterman Beach", "wave_height"],
]

menorah = Menorah(
  sources,
  "work/debris", 
  since=datetime(2015, 5, 20)
)

menorah.swarm()
menorah.runModel()

# Graffiti Removal vs weather.

sources =  [
  ["chicago-311", "Graffiti Removal", "aggregate=1 day"],
  ["chicago-beach-weather", "Foster Weather Station", "humidity"],
  ["chicago-beach-weather", "Foster Weather Station", "interval_rain"],
  ["chicago-beach-weather", "Foster Weather Station", "barometric_pressure"],
  ["chicago-beach-weather", "Foster Weather Station", "wind_speed"],
  ["chicago-beach-weather", "Foster Weather Station", "maximum_wind_speed"],
  ["chicago-beach-weather", "Foster Weather Station", "air_temperature"],
]

menorah = Menorah(
  sources,
  "work/graffiti", 
  since=datetime(2015, 5, 20)
)

menorah.swarm()
menorah.runModel()

# Rodent Baiting vs weather.

sources =  [
  ["chicago-311", "Rodent Baiting", "aggregate=1 day"],
  ["chicago-beach-weather", "Foster Weather Station", "humidity"],
  ["chicago-beach-weather", "Foster Weather Station", "interval_rain"],
  ["chicago-beach-weather", "Foster Weather Station", "barometric_pressure"],
  ["chicago-beach-weather", "Foster Weather Station", "wind_speed"],
  ["chicago-beach-weather", "Foster Weather Station", "maximum_wind_speed"],
  ["chicago-beach-weather", "Foster Weather Station", "air_temperature"],
]

menorah = Menorah(
  sources,
  "work/rodents", 
  since=datetime(2015, 5, 20)
)

menorah.swarm()
menorah.runModel()
