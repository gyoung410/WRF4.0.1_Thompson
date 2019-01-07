from netCDF4 import Dataset
import wrf
import xarray as xr
import numpy as np

import matplotlib
import matplotlib.cm as mpl_cm
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import cartopy.crs as crs
import cartopy.feature as cfe

###################################
## Load in WRF data
###################################

root_dir = '/data/mac/giyoung/MAC_WRFThompson/'
nc = Dataset(root_dir+'2_Nisg80_ThompsonDefault/wrfout_d01_2015-11-27_00:00:00')
qnifa = wrf.getvar(nc, 'QNIFA', timeidx=32)

## Quick Plot to check all is well
# qnifa.plot()

## Get the latitude and longitude points
lats, lons = wrf.latlon_coords(qnifa)

## Get the cartopy mapping object
cart_proj = wrf.get_cartopy(qnifa)

# data = wrf.to_np(qnifa[0,:,:])
data = wrf.to_np(qnifa[0,:,:])

# Create a figure
fig = plt.figure(figsize=(6,5))
# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Add coastlines
ax.coastlines('50m', linewidth=0.8)
ax.add_feature(cfe.NaturalEarthFeature('physical', 'antarctic_ice_shelves_lines', 
                                       '50m', linewidth=1.0, edgecolor='k', facecolor='none') )

# Plot contours
plt.contourf(wrf.to_np(lons), wrf.to_np(lats), data, 10, 
                transform=crs.PlateCarree(), cmap = mpl_cm.Reds)

# Add a color bar
cbar = plt.colorbar(ax=ax, shrink=.62)
cbar.set_label(qnifa.units)

# Set the map limits.  Not really necessary, but used for demonstration.
ax.set_xlim(wrf.cartopy_xlim(qnifa))
ax.set_ylim(wrf.cartopy_ylim(qnifa))

# Add the gridlines
ax.gridlines(color="black", linestyle="dotted")

plt.title(qnifa.description+'\n'+str(qnifa.Time.values))

plt.show()