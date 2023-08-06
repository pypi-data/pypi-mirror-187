# Geostream

**Geostream** is a Python tool to interact with OGC APIs with ease and download geospatial data to Geopandas GeoDataFrames. 

**Status**: Currently only works with WFS API and is very experimental by nature. Use at own risk. 

## Installation

`geostream` is available via PyPi and can be installed with:

- `pip install geostream`

## Basic usage

```python
from geostream import WFS

# Endpoint for WFS API of the City of Helsinki
endpoint = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs"

# Initialize WFS reader 
# Note: API version can vary between data providers (by default 1.0.0 is used) 
wfs = WFS(endpoint, version="2.0.0")

# See all available layers
wfs.get_layers()

# Store the id of the first layer
first_layer = wfs.get_layers()[0]

# Find info for specific layer
wfs.get_layer_info(first_layer)

# Download a GeoDataFrame with Helsinki as the extent
helsinki_gdf = wfs.get_gdf_from_place("Helsinki")

# Download the data into GeoDataFrame from the Helsinki Region
data = wfs.load_wfs(layer_id=first_layer, bounding_box=helsinki_gdf)
```