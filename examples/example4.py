# Just an example of how to fetch River View data into a CSV so you can process
# it yourself. 

from menorah import Menorah

sources =  [
  ["mn-traffic-sensors", "T4013", "speed"],
  ["mn-traffic-sensors", "1036", "speed"],
  ["mn-traffic-sensors", "1187", "speed"],
]

menorah = Menorah(sources, "work/example4-data-only")
menorah.populateCsv()

# Find CSV at "work/example4-data-only/data.csv".