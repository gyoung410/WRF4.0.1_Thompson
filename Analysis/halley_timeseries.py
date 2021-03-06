##-----------------------------------------------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------------------------------------------
# The first line in a time-series output looks like this:
#
# 	NZCM McMurdo               2  7 mcm   (-77.850, 166.710) ( 153, 207) (-77.768, 166.500)   81.8 meters
#
# 	Those are name of the station, grid ID, time-series ID, station lat/lon, grid indices (nearest grid point to
# 	the station location), grid lat/lon, elevation.
#
# 	The variables from the time series output are:
#
# 	id, ts_hour, id_tsloc, ix, iy, t, q, u, v, psfc, glw, gsw, hfx, lh, tsk, tslb(1), rainc, rainnc, clw
#
# 	id:             grid ID
# 	ts_hour:        forecast time in hours
# 	id_tsloc:       time series ID
# 	ix,iy:          grid location (nearest grid to the station)
# 	t:              2 m Temperature (K)
# 	q:              2 m vapor mixing ratio (kg/kg)
# 	u:              10 m U wind (earth-relative)
# 	v:              10 m V wind (earth-relative)
# 	psfc:           surface pressure (Pa)
# 	glw:            downward longwave radiation flux at the ground (W/m^2, downward is positive)
# 	gsw:            net shortwave radiation flux at the ground (W/m^2, downward is positive)
# 	hfx:            surface sensible heat flux (W/m^2, upward is positive)
# 	lh:             surface latent heat flux (W/m^2, upward is positive)
# 	tsk:            skin temperature (K)
# 	tslb(1):        top soil layer temperature (K)
# 	rainc:          rainfall from a cumulus scheme (mm)
# 	rainnc:         rainfall from an explicit scheme (mm)
# 	clw:            total column-integrated water vapor and cloud variables
##-----------------------------------------------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------------------------------------------

import numpy as np

import matplotlib
import matplotlib.cm as mpl_cm
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import cartopy.crs as crs
import cartopy.feature as cfe

import pandas as pd

###################################
## Load in data
###################################

## 2_Nisg80_ThompsonDefault/
## 3_Nisg80_ThompsonAeroClim/
## 4_Nisg80_Thompson_naCCN0408_naCCN1100/
## 5_Archer_Default_AeroClim/
## 6_Archer_INITpl100e6/
## 7_Archer_INITpl100/
## 8_Archer_INITpl100_DRIVERpl100/
## 9_Archer_DRIVER_NWFA1D_100e6/
## 10_Archer_DRIVER_NWFA1D_100/
## 11_Archer_DRIVER_NWFA1D_100e3/
## 12_Archer_DRIVER_NWFA1D_x2/	# FAILED JOB - ERROR
## 13_Archer_DRIVER_NWFA1D_x05/
## 14_Archer_DRIVER_NWFA1D_150e3/
## 15_Archer_DRIVER_NWFA1D_150e3_K1/
## 16_Archer_DRIVER_NWFA1D_100e3_K1/

file_dir1 = '2_Nisg80_ThompsonDefault/'
file_dir2 = '3_Nisg80_ThompsonAeroClim/'

index = 'gsw'

# root_dir = '/gws/nopw/j04/ncas_weather/gyoung/MAC/WRF_V4.0.1/RUNS/'
root_dir = '/data/mac/giyoung/MAC_WRFThompson/' # BAS SCIHUB


###################################
## d01
###################################
filename1 = "".join(root_dir+file_dir1+'hal.d02.TS')
file1 = np.loadtxt(filename1,skiprows=1)
df1 = pd.DataFrame(file1)

###################################
## d02
###################################
filename2 = "".join(root_dir+file_dir2+'hal.d02.TS')
file2 = np.loadtxt(filename2,skiprows=1)
df2 = pd.DataFrame(file2)

###################################
## Quick check
###################################

df1.iloc[0,:] # prints first row of data
df1.head()

# data1 = df.values
# data1[0,0] ## first value
# df.columns ## headers

###################################
## Set column names
###################################

df1.columns = ['id','ts_hour','id_tsloc','ix','iy','t','q','u','v','psfc','glw','gsw','hfx','lh','tsk','tslb(1)','rainc','rainnc','clw']
df2.columns = ['id','ts_hour','id_tsloc','ix','iy','t','q','u','v','psfc','glw','gsw','hfx','lh','tsk','tslb(1)','rainc','rainnc','clw']

###################################
## Ignore 1st 24 hours (spin up)
###################################


SMALL_SIZE = 14
MED_SIZE = 16
LARGE_SIZE = 18

plt.rc('font',size=MED_SIZE)
plt.rc('axes',titlesize=MED_SIZE)
plt.rc('axes',labelsize=MED_SIZE)
plt.rc('xtick',labelsize=SMALL_SIZE)
plt.rc('ytick',labelsize=SMALL_SIZE)
plt.rc('legend',fontsize=SMALL_SIZE)
# plt.rc('figure',titlesize=LARGE_SIZE)

## create figure and axes instances
fig = plt.figure(figsize=(6,5))

ax  = fig.add_axes([0.2,0.15,0.7,0.7])	# left, bottom, width, height

plt.plot(df1.loc[np.size(df1.values[:,0])/float(2)-1:,'ts_hour']-24,df1.loc[np.size(df1.values[:,0])/float(2)-1:,index],label = 'Default')
plt.plot(df2.loc[np.size(df2.values[:,0])/float(2)-1:,'ts_hour']-24,df2.loc[np.size(df2.values[:,0])/float(2)-1:,index],label = 'AeroClim')
plt.xlabel('Time, h [27-Nov-2018]')
plt.ylabel(index)
plt.xlim([0,24])
plt.legend()
plt.savefig('FIGS/Halley_GSW_timeseries.png',dpi=300)
plt.show()
