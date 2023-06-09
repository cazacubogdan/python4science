# python4science
 Various python scripts usefull for science

| solar-simulation.py |
Rendering the entire solar system in real-time, including physics simulation for each object, is a complex task that requires a lot of computational power. However, we can create a simplified simulation that includes the major bodies in the solar system and their orbits. This script uses the `PyOpenGL` library to create a window and draw the solar system. It defines the simulation parameters, including the size and distance of each object, and the speed at which they rotate. It also defines the colors for each object. The `draw_sphere` function is used to draw a sphere with a given radius and color. The `draw_solar_system` function calculates the positions and orientations of the objects based on the current date and time, and then draws them using `draw_sphere`. The `display` function is used to clear the screen and draw the solar system. The `idle` function is used to update the simulation by updating the rotation angles and positions of the objects. Finally, the `main` function initializes the window and sets up the display and idle functions. It then enters the main loop of the application, which processes user input and updates the display and simulation as necessary.

| render-tetrahedron.py |
To render a tetrahedron in Python, we can use a 3D graphics library such as matplotlib (used), Mayavi, or OpenGL. This script defines the vertices and faces of the tetrahedron, creates a Poly3DCollection object from them, and adds it to a 3D axis object. It then sets the axis limits and labels, and displays the plot using plt.show()

| astro-stacker.py |
Python script using the astropy package to stack your images. This script assumes that all the images are in the same directory and are named image1.fits, image2.fits, and so on up to image10000.fits. You may need to modify the script to match your file naming convention. The script first loads the header and WCS information from the first image in the set to ensure that all the images are aligned correctly. It then calculates the median of the data values for each pixel across all the images, which effectively reduces the noise in the final image. It uses sigma_clipped_stats from astropy.stats to calculate the standard deviation and mean of the data values for each pixel. It then creates a Cutout2D object centered on the astronomical object and saves it to a new FITS file, along with some header information about the stack. Note that the size of the Cutout2D object is set to 100 pixels in this example, but you may need to adjust this value based on the size of your object and the resolution of your images.

| remote-outpost-uploader.py | Python script that monitors for new files in a specified directory, adds them to a queue for uploading to a remote SSH server (either via username and password or via ssh-key), and can handle network interruptions and bandwidth limiting. It uses the Paramiko library for SSH and the Watchdog library for monitoring file system events.

To use SSH key authentication, save the private key file to the same directory as the script and execute the following command in a terminal:
python remote-outpost-uploader.py /path/to/directory --key private_key.pem --limit 100
Replace /path/to/directory with the path to the directory you want to monitor for new files, and --limit with the desired bandwidth limit in kbps (optional).

