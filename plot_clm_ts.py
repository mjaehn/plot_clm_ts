
# Define netcdf filename

import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm

# Define the netCDF filename
nc_file = '/scratch/snx3000/mjaehn/CH2025/spice/chain/work/cordex_12km_era5_gpu_20230317/post/1985_07/CLCT_ts.nc'

# Open the netCDF file and extract the necessary variables
with netCDF4.Dataset(nc_file, 'r') as ds:
    clct_var = ds.variables['CLCT']
    lat_var = ds.variables['lat']
    lon_var = ds.variables['lon']
    time_var = ds.variables['time']

    # Extract the relevant attributes
    fill_value = clct_var._FillValue
    long_name = clct_var.long_name
    units = clct_var.units
    lat_min = np.min(lat_var)
    lat_max = np.max(lat_var)
    lon_min = np.min(lon_var)
    lon_max = np.max(lon_var)

    # Define the projection
    proj = Basemap(projection='mill', lat_ts=10, llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='c')

    # Create the figure and axis for the plot
    fig, ax = plt.subplots()

    # Define the contour levels for the plot
    levels = np.arange(0, 101, 10)

    # Define the function to animate the plot
    def animate(i):
        # Clear the previous plot
        ax.clear()

        # Get the cloud cover data for the current time step
        clct = clct_var[i, :, :]

        # Replace the fill value with NaN
        clct = np.where(clct == fill_value, np.nan, clct)

        # Plot the data on the map
        x, y = proj(lon_var[:], lat_var[:])
        clevs = np.arange(0, 110, 10)
        cs = proj.contourf(x, y, clct, levels=clevs, cmap='Blues_r', extend='max')
        proj.drawcoastlines()
        proj.drawcountries()
        proj.drawmeridians(np.arange(lon_min, lon_max, 10), labels=[False,False,False,True])
        proj.drawparallels(np.arange(lat_min, lat_max, 10), labels=[True,False,False,False])

        # Add a title to the plot
        ax.set_title(f'{long_name} at time {i} ({time_var[i]})')

        # Return the plot
        return cs

    # Create the animation
    anim = FuncAnimation(fig, animate, frames=10, interval=100, blit=False)

    # Save the animation as a gif
    anim.save('CLCT_ts.gif', writer='imagemagick')

    # Print a message to indicate the animation is created
    print('Animation created!')

    # Show the plot
    plt.show()

