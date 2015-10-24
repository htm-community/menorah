from datetime import datetime

from menorah import Menorah


dataIds =  [
  ["mn-traffic-sensors", "618", "occupancy"],
  ["mn-traffic-sensors", "678", "occupancy"],
  ["mn-traffic-sensors", "730", "occupancy"],
  ["mn-traffic-sensors", "677", "occupancy"],
  ["mn-traffic-sensors", "670", "occupancy"],
  ["mn-traffic-sensors", "731", "occupancy"],
  ["mn-traffic-sensors", "727", "occupancy"],
  ["mn-traffic-sensors", "728", "occupancy"],
  # ["yahoo-finance-prices", "AAPL", "Volume"],
  # ["yahoo-finance-prices", "GOOG", "Volume"],
  # ["yahoo-finance-prices", "MSFT", "Volume"],
  # ["yahoo-finance-prices", "NFLX", "Volume"],
  # ["yahoo-finance-prices", "TSLA", "Volume"],
  # ["yahoo-finance-prices", "YHOO", "Volume"],
  # ["ercot-demand", "system_wide_demand", "Demand"],
  # ["airnow", "Austin, TX", "Ozone"],
  # ["airnow", "Beaumont-Port Arthur, TX", "Ozone"],
  # ["airnow", "Brownsville-McAllen, TX", "Ozone"],
]

startAt = datetime(2015, 1, 1)

menorah = Menorah(dataIds, since=startAt, limit=5000)

runNupic = True

if runNupic:
  menorah.swarm(
    "work/traffic", 
    swarmParams={"swarmSize": "small"}
  )
  menorah.runModel("work/traffic")

else:
  # Prototype for streaming all data into a function.
  def handleRow(headers, data):
    print ",".join([str(d) for d in data])

  menorah.stream(handleRow)
