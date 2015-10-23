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
]

startAt = datetime(2015, 8, 1)

menorah = Menorah(dataIds, since=startAt)

# Prototype for writing all data rows to CSV.
menorah.writeCsv("just-a-test.csv")


# Prototype for streaming all data into a function.
def handleRow(headers, data):
  pass

menorah.stream(handleRow)

