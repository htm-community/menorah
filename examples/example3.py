# Gets aggregated data for Portland OR 911 calls and attempts to predict the 
# number of calls every 15 minutes.

from datetime import datetime

from menorah import Menorah

sources =  [
  ["portland-911", "portland-911", "aggregate=15 minutes"],
]

menorah = Menorah(sources, "work/example3-aggregated", since=datetime(2015, 7, 10))
menorah.swarm()
menorah.runModel(plot=True)
