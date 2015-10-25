from menorah import Menorah

sources =  [
  ["ercot-demand", "system_wide_demand", "Demand"],
  ["airnow", "Austin, TX", "Ozone"],
  ["airnow", "Beaumont-Port Arthur, TX", "Ozone"],
  ["airnow", "Brownsville-McAllen, TX", "Ozone"],
]

menorah = Menorah(sources, "work/traffic")
menorah.swarm()
menorah.runModel()