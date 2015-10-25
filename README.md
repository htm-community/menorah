# Menorah

![Menorah logo](menorah.png)

It's easy to run [NuPIC](http://github.com/numenta/nupic) on live real-world data with Menorah. Menorah's data is powered by [River View](http://data.numenta.org), which is a [NuPIC Community](http://github.com/nupic-community/river-view) temporal data store.
 
## Find Data

Take the data feed [`http://data.numenta.org/ercot-demand/system_wide_demand/data.html`](http://data.numenta.org/ercot-demand/system_wide_demand/data.html)...

The pattern is `/<river-name>/<stream-name>/data.[json|html|csv]`, so we can create, swarm, and run a NuPIC model on this data stream easily.

```python
from menorah import Menorah

experimentDir = "nupic-experiments/ercot"
sources = [
  ["ercot-demand", "system_wide_demand", "Demand"],
]

menorah = Menorah(sources, experimentDir)
menorah.swarm()
menorah.runModel()
```