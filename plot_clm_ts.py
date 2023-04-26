import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap
import glob
import sys

# Define the netCDF filename
varname = 'CLCT'
datadir = '/project/d121/mjaehn/cordex_12km_era5_gpu_20230317/post'
nc_files = sorted(glob.glob(datadir + '/1988_07/' + varname + '_ts.nc'))

# Define the output directory for the plots
outdir = '/scratch/snx3000/mjaehn/CH2025/plots/' + varname

# Open the netCDF file and extract the necessary variables
for nc_file in nc_files:
    with nc.Dataset(nc_file, 'r') as ds:
        clct_var = ds.variables['CLCT']
        lat_var = ds.variables['lat']
        lon_var = ds.variables['lon']
        time_var = ds.variables['time']
        lon_0 = ds.variables['rotated_pole'].north_pole_grid_longitude
        o_lat_p = ds.variables['rotated_pole'].grid_north_pole_latitude
        o_lon_p = ds.variables['rotated_pole'].grid_north_pole_longitude

        # Extract the relevant attributes
        fill_value = clct_var._FillValue
        long_name = clct_var.long_name
        units = clct_var.units
        time_units = time_var.units
        time_calendar = time_var.calendar
        num_times = len(time_var)
        lat_min = np.min(lat_var)
        lat_max = np.max(lat_var)
        lon_min = np.min(lon_var)
        lon_max = np.max(lon_var)

        # Define the projection
        proj = Basemap(projection='mill',
                       lat_ts=10,
                       llcrnrlon=lon_min, 
                       urcrnrlon=lon_max, 
                       llcrnrlat=lat_min, 
                       urcrnrlat=lat_max,
                       resolution='c')

        # Define the contour levels and labels
        clevs = np.arange(0, 110, 10)

        # Create the initial plot and colorbar
        fig, ax = plt.subplots()
        x, y = proj(lon_var[:], lat_var[:])
        cmap = 'Blues'
        cs = proj.contourf(x, y, clct_var[0, :, :], levels=clevs, cmap=cmap, extend='max')
        cbar = plt.colorbar(cs, ax=ax, orientation='horizontal')
        cbar.set_label('Cloud Cover (%)')

        # Add a legend to the plot
        legend = ax.legend(loc='lower left', bbox_to_anchor=(0.0, -0.4), ncol=6, frameon=False)

        # Loop over each time step and save a plot to a file
        for i in range(num_times):
            # Get the cloud cover data for the current time step
            clct = clct_var[i, :, :]

            # Replace the fill value with NaN
            clct = np.where(clct == fill_value, np.nan, clct)

            # Plot the data on the map
            cs = proj.contourf(x, y, clct, levels=clevs, cmap=cmap, extend='max')
            proj.drawcoastlines(linewidth=1)
            proj.drawcountries()
            proj.drawmeridians(np.arange(-90, 90, 20), linewidth=0.5, labels=[False,False,False,True])
            proj.drawparallels(np.arange(-180, 180, 10), linewidth=0.5, labels=[True,False,False,False])

            # Convert the time value to a human-readable format
            time_value = nc.num2date(time_var[i], units=time_units, calendar=time_calendar)

            # Add a title to the plot
            ax.set_title(f'{long_name} at {time_value.strftime("%Y-%m-%d %H:%M:%S")}')

            # Save the plot to a file
            fn_plot = f'{outdir}/clct_{time_value.strftime("%Y%m%dT%H%M%S")}.png'
            plt.savefig(fn_plot, bbox_inches='tight', dpi=120)
            print(f'{fn_plot} written!')

            # Clear the plot for the next time step
            ax.clear()

        # Close the figure
        plt.close(fig)
