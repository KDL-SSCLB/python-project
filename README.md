# python-project

This repository has the python code (plotVertJumpCSV.py) and datafile (P1VertJump_to.csv) that
I used to make a figure of

1. sagittal view (right side) stick figure or person doing a vertical jump from start of 
  motion to take-off using 3D motion capture data.  The 'subject' model only had trunk, pelvis, and 
  right and left legs.  No arms or head.  The motion capture data came from a data collection using Vicon Nexus
  of a real person doing a two footed maximal effort vertical jump.  The csv file has the exported x (medial-lateral), y (anterior-posterior)
  and z (vertical) coordinates of all the markers on the body.  Data were collected at 120 fps.

2. plot of vertical position of center of mass (COM). COM was calculated using foot, lower leg, thigh, and HAT (head, arms, and trunk) segment 
  using data from Dempster

3 plot of vertical velocity of COM.  Velocity was calculated using central difference method in a for loop.  Velocity data was filtered in a
  quick and easy for loop using a 9-point moving average filter.  The first 4 and last 4 points were padded of the filtered data were padded with NaN

The plots were animated with an interactive figure using a for loop to update the x and y data for each line.

1. For the stick figure, both the stick figure and a dot and COM are visualized as the plot is updated each iteration showing the next sample (row) of data
2. The COM position and Velocity graphs had a red dot whose position updates throughout the loop so that you can visualize where you are on the
   graph synchronized with the visualization of the stick figure

IMPORTANT
1. Place the data file in the same folder as the code.  Or you can 'uncomment' the input statement asking for a filename and then enter the path+filename
to when prompted as appropriate.

3. You will need to install pandas, matplotlib, and numpy


