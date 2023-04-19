import imageio
import os

# Set the directory where your PNG files are located
directory = '/path/to/png/files'

# Create a list of the file names in the directory
file_names = os.listdir(directory)

# Sort the file names by date (assuming the files are named according to a date format)
file_names = sorted(file_names)

# Create an imageio writer object to write the animation as an MP4 file
writer = imageio.get_writer('animation.mp4', mode='FFMPEG', fps=2)

# Iterate over the sorted file names and add each frame to the animation
for file_name in file_names:
    image = imageio.imread(os.path.join(directory, file_name))
    writer.append_data(image)

# Close the writer object to finish writing the animation
writer.close()
