import csv
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
 
#Could midofy to ask for file
#fname=input('Enter the file you want to open (e.g. P1vertJump_to.csv): ')
fname='P1VertJump_to.csv'
print("Reading File:", fname)

#Since csv file is irregualr, open in line by line use csv reader and append each row into
#a variable called data
data = []
with open(fname, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data.append(row)

#get sampling rate from line 2 of the file that was read in
#and then calculate time interval  from teh sampling rate
srate=int(data[1][0])
deltat=1/srate

#make a pandas data frame from the data
data2 = pd.DataFrame(data)

#crop out the first 5 header rows 
#Get Right side of body AP (y coordinate but call it x) and Vert (Z coordinate)
#but call it y) segment endpoints and Create column labels

#Make 2D array for x coodinates first
data3=data2.iloc[5:len(data2)-1,:]
datax=data3[[126,57,39,18, 21,117]]
datax = datax.astype(float)
datax.columns=['RTOEX', 'RHEELX','RANKX', 'RKNEEX',  
               'RHIPX', 'RSHLDX' ]
datax = datax.to_numpy()
datax=datax/1000

#y cooridantes
datay=data3[[127,58,40,19, 22,118]]
datay = datay.astype(float)
datay.columns=[ 'RTOEY', 'RHEELY', 'RANKY', 'RKNEEY', 
                'RHIPY','RSHLDY']
datay=datay.to_numpy()
datay=datay/1000

#Find COM location of each segmentusing Dempster data
footx=(datax[:,0]-datax[:,2])*.5 +datax[:,2]
footy=(datay[:,0]-datay[:,2])*.5 +datay[:,2]
legx=(datax[:,2]-datax[:,3])*.433 +datax[:,3]
legy=(datay[:,2]-datay[:,3])*.433 +datay[:,3]
thighx=(datax[:,3]-datax[:,4])*.433 +datax[:,4]
thighy=(datay[:,3]-datay[:,4])*.433 +datay[:,4]
HATx=(datax[:,4]-datax[:,5])*.626 +datax[:,5]
HATy=(datay[:,4]-datay[:,5])*.626 +datay[:,5]

#FInd while body COM lcoation
COMX=(footx*.0145+legx*.0165+thighx*.1+HATx*.678)/(.0145+.0165+.1+.678)
COMY=(footy*.0145+legy*.0165+thighy*.1+HATy*.678)/(.0145+.0165+.1+.678)

#Make a time series for plotting pruposes
t=np.arange(start=0,stop=len(COMY)*deltat,step=deltat) # time in s

#Create zero 1D array for calcuating COM vertical velocity
COMYVEL=np.zeros(len(COMY))

#use a loop to get vertical velocity using central difference method
for i in range(len(COMY)-1):
    if i==0 or i==len(COMY)-1:
        COMYVEL[i]=(COMY[i+1]-COMY[i])/(deltat)    
    else:
        COMYVEL[i]=(COMY[i+1]-COMY[i-1])/(2*deltat)
 

#create a zero 1D array for filtered COMYVel
COMYVELfilt=np.zeros(len(COMYVEL)-8)

#Get a quick and dirty 9 point moving average filter. Using a for loop
#time series wil be 8 poinst shorter since can't filter 1st 4 or first last points
for i in range(4, len(COMYVELfilt)+4):
    COMYVELfilt[i-4]=sum(COMYVEL[i-4:i+4])/9

#pad COMYVELfilt to make array back to original length for ploting purposes 
#in iteration for loop
COMYVELfilt=np.pad(COMYVELfilt,(4,4),mode='constant', constant_values=np.nan)


#calculate jump height using unifmorlay accelerated motion
#take-off frame is 15 before end of file length (but indeices start at 0, so subtract 16
#TO row)
TOVEL=COMYVELfilt[len(COMYVELfilt)-16]
Ht=(TOVEL**2)/(2*9.81)
Ht_in=Ht/.0254
Ht=round(Ht, 2)
Ht_in=round(Ht_in, 2)

# enable interactive mode
plt.ion()

#create figure with sub figures and axes objects on each subfigure
fig = plt.figure(figsize=(10, 6))
(leftfig, rightfig)=fig.subfigures(1,2)
ax1=leftfig.subplots(1,1)
leftfig.subplots_adjust(left=.1, right=.9, bottom=0.1, top=.85)
right_axs=rightfig.subplots(2,1)
rightfig.subplots_adjust(hspace=0.4, left=0.1, right=.9, bottom=.1, top=.85)
ax2=right_axs[0]
ax3=right_axs[1]
leftfig.text(0.5, 0.05, 'Jump Height = {} meters or {} inches'.format(Ht, Ht_in), 
             horizontalalignment='center', fontsize=12, wrap=True ) 


# configure axes axis range, titles, lables, and formatting
ax1.set_xlim([-.9,.9])
ax1.set_ylim([-0,1.8])
ax1.set_title('Vertical Jump Propuslive Phase')
ax1.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
ax2.set_xlim([0,max(t)])
ax2.set_ylim([0,1.8])
ax2.set_title('COM Vertical Position')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('meters')
ax3.set_xlim([0,max(t)])
ax3.set_ylim([min(COMYVELfilt[4:len(COMYVELfilt)-4]),max(COMYVELfilt[4:len(COMYVELfilt)-4])])
ax3.set_title('COM Vertical Velocity')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('meters/second')
ax3.set_xlim([0,max(t)])
yaxis=ax3.get_yticks()    
ax3.set_yticks(yaxis)
ax3.set_yticklabels([f'{label:.1f}' for label in yaxis])

#Get 1st data points to be plot prior to iterating for teh 3 axes
# x and y are farme 1 of the stick figure, line 1 is stickfigure, line 2 is com dot (line 1 and 2 iteratre)
x=datax[0]
y=datay[0]
line, =ax1.plot(x,y, color='blue')
line2,=ax1.plot(COMX[0],COMY[0], marker='o', linestyle='none', color='red')

#line3 is com vertical position and line 4 is dot on the graph that will iteratre
line3, =ax2.plot(t,COMY, color='blue')
line4, =ax2.plot(t[0],COMY[0], marker='o', color='red')

#line5 is com vertical position and line 6 is dot on the graph that will iteratre
line5, =ax3.plot(t,COMYVELfilt, color='blue')
line6, =ax3.plot(t[4],COMYVELfilt[4], marker='o', color='red')

#loop that iteratre trhough each row (data sample) redrawing stickfigure, COM, for ax1 and
#drawing dot on axes 2 and 3 at time location fo iteration
for i in range(len(datax)):
        line.set_xdata(datax[i])
        line.set_ydata(datay[i])
        line2.set_xdata([COMX[i]])
        line2.set_ydata([COMY[i]])
        line4.set_xdata([t[i]])
        line4.set_ydata([COMY[i]])
        line6.set_xdata([t[i]])
        line6.set_ydata([COMYVELfilt[i]])
        fig.canvas.draw()
        fig.canvas.flush_events()

     
