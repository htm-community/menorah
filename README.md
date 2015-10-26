# Menorah

> Menorah is a [NuPIC](http://github.com/numenta/nupic) experiment framework for [River View](http://data.numenta.org).

![Menorah logo](menorah.png)

It's easy to run [NuPIC](http://github.com/numenta/nupic) on live real-world data with Menorah. Menorah's data is powered by [River View](http://data.numenta.org), which is a [NuPIC Community](http://github.com/nupic-community/river-view) temporal data store.
 
## Data delivered directly to NuPIC

To stream data from River View into NuPIC, you need to know the `river`, `stream`, and `field` for each data feed. 

Take the data feed [`http://data.numenta.org/ercot-demand/system_wide_demand/data.html`](http://data.numenta.org/ercot-demand/system_wide_demand/data.html):

The pattern is `/<river>/<stream>/data.html`. To find the `field`, look at [River View HTML interface](http://data.numenta.org/ercot-demand/system_wide_demand/data.html) to decide what data field is desired. 

Each one is a list `[river, stream, field]`, and they are provided to the `Menora` constructor in a list. For example:

```python
from menorah import Menorah

sources = [
  ["ercot-demand", "system_wide_demand", "Demand"],
]

menorah = Menorah(sources, "experiments/")
menorah.swarm()
menorah.runModel()
```

## Working Directory

Menorah needs a working directory for its second constructor parameter, because NuPIC writes artifacts to the file system. Pass in a path to a working folder for menorah experiments.

## Run multiple fields

I recommend running less than 8 fields in a single model, but you can configure as many as you wish. 

```python
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
```

## View the predictions

You can find a `predictions.csv` file in the working directory you specified. Or you can call `runModel(plot=True)` to plot with matplotlib.
