# Menorah

> Menorah is a [NuPIC](http://github.com/numenta/nupic) experiment framework for [River View](http://data.numenta.org).

![Menorah logo](menorah.png)

It's easy to run [NuPIC](http://github.com/numenta/nupic) on live real-world data with Menorah. Menorah's data is powered by [River View](http://data.numenta.org), which is a [NuPIC Community](http://github.com/nupic-community/river-view) temporal data store.

## Installation

First, you must install [NuPIC](http://github.com/numenta/nupic) however you wish. Then you can run:

    pip install menorah
 
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

menorah = Menorah(sources, "experiments/ercot")
menorah.swarm()
menorah.runModel()
```

## Working Directory

Menorah needs a working directory for its second constructor parameter, because NuPIC writes artifacts to the file system. Pass in a path to a working folder for menorah experiments.

## Run multiple fields

I recommend running less than 8 fields in a single model, but you can configure as many as you wish. The example below attempts to better predict the number of "tree debris" 311 calls in Chicago and incorporates data from local weather stations. It also shows an example of aggregating a geospatial data feed to get event counts within an aggregation period. 

```python
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

menorah.swarm(swarmParams={"swarmSize":"large"})
menorah.runModel(plot=True)

```

## View the predictions

You can find a `predictions.csv` file in the working directory you specified. Or you can call `runModel(plot=True)` to plot with matplotlib.

## Pro Tips

- For `geospatial` data streams like [portland-911](http://data.numenta.org/portland-911/portland-911/data.html), you can aggregate counts of events by providing an *aggregation string* instead of a `field` name. See [example5.py](examples/example5.py) and `aggregate=1 day` in the `sources` list. 
- Once you've swarmed once on a particular experiment, you can comment out the call to `swarm()` on subsequent runs.

## TODO

- Save `Menorah` instances, which should save the underlying model and the data cursors so the may be continued from the point where they left off.
