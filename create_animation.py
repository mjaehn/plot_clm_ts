import imageio
import os
import glob

# Set the directory where your PNG files are located
directory = '/scratch/snx3000/mjaehn/CH2025/plots/CLCT'
outfile = '/scratch/snx3000/mjaehn/CH2025/plots/clct_198807.gif'

# Create a list of the file names in the directory
file_names = sorted(glob.glob(directory + '/clct_198807*.png'))

# Create an imageio writer object to write the animation as an MP4 file
writer = imageio.get_writer(outfile, mode='I', fps=24)

# Iterate over the sorted file names and add each frame to the animation
for file_name in file_names:
    print(f'Processing {file_name}')
    image = imageio.imread(os.path.join(directory, file_name))
    writer.append_data(image)

# Close the writer object to finish writing the animation
writer.close()
