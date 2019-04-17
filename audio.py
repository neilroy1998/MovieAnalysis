from subprocess import check_output
import datetime
from numpy.fft import *
from numpy import log10, sqrt, array, zeros, ones, multiply
import math
import wave
import struct
import matplotlib.pyplot as plt
import os
import csv
#Thanks to: https://cshorde.wordpress.com/2014/09/05/start-audio-in-python/

os.chdir(r'C:\Users\neilr\Documents\dmpaProjAudio'.replace('\\','//'))

filevid = input("Enter Video File: ")
filename = filevid.split(".")[0]
label = input("Add Label: ")

is_stamp = int(input("Do you want for specific timestamps?\n(1) for Yes\n(2) for full clip\n"))

def time_subtract(s,e):
	frmt='%H:%M:%S'
	startT=datetime.datetime.strptime(s, frmt)
	endT=datetime.datetime.strptime(e, frmt)
	return str(endT-startT)

if is_stamp==1:
	start = input("Enter start time in format hh:mm:ss\n")
	end = input("Enter end time in format hh:mm:ss\n")
	dur=time_subtract(start,end)
elif is_stamp==2:
	start = "00:00:00"
	end = str(check_output('ffprobe -i  "'+filevid+'" 2>&1 |findstr "Duration"',shell=True)) 
	end = end.split(",")[0].split("Duration:")[1].strip()
	end = end.split('.')[0]
	dur=time_subtract(start,end)

fileout = '"'+filename+'_'+label+'.mp3"'
out = str(check_output('ffmpeg -i "'+filevid+'" -ss '+start+' -t '+dur+' -q:a 0 -map a '+fileout,shell=True))

print("\nConverting to .WAV\n")

fileoutWAV = fileout.split(".")[0]+'.wav"'
out = str(check_output('ffmpeg -i '+fileout+' '+fileoutWAV,shell=True))

"""
Turn a wave file into an array of ints
Wav file should not contain Metadata
"""
def get_samples(file):
     
    file = file.replace('"','')
    waveFile = wave.open(file, 'r')
    samples = []
    samples_duo = []
 
    # Gets total number of frames
    length = waveFile.getnframes()
     
    # Read them into the frames array
    for i in range(0,length):
        waveData = waveFile.readframes(1)
        data = struct.unpack("%ih"%2, waveData)
         
        # After unpacking, each data array here is actually an array of ints
        # The length of the array depends on the number of channels you have
         
        # Drop to mono channel
        x=abs(int(data[0]))
        samples.append(x)
        samples_duo.append(int(data[0]))
     
    samples = array(samples)
    return samples

def get_samples_duo(file):
     
    file = file.replace('"','')
    waveFile = wave.open(file, 'r')
    samples = []
 
    # Gets total number of frames
    length = waveFile.getnframes()
     
    # Read them into the frames array
    for i in range(0,length):
        waveData = waveFile.readframes(1)
        data = struct.unpack("%ih"%2, waveData)
         
        # After unpacking, each data array here is actually an array of ints
        # The length of the array depends on the number of channels you have
         
        # Drop to mono channel
        samples.append(int(data[0]))
     
    samples = array(samples)
    return samples

nos = get_samples(fileoutWAV)
nos_duo = get_samples_duo(fileoutWAV)
print(nos)
print(nos_duo)

length = len(nos)
length_duo = len(nos_duo)

new_nos = nos.copy()
new_nos_duo = nos_duo.copy()

for i in range (0,length):
	if (i<0):
		new_nos[i]=-1
	else:
		new_nos[i]=nos[i]//5000

for i in range (0,length_duo):
	if (i<0):
		new_nos_duo[i]=-1
	else:
		new_nos_duo[i]=nos_duo[i]//5000

print("\n\nClassified:\n")
print(new_nos)
print(new_nos_duo)

#is_plot = int(input("\n\nDo you want a plot? (0/1)\n"))
#if is_plot:
#	plt.plot(nos)
#	plt.plot(new_nos)
#	plt.show()

print("\n\nFor Per Second now\n")
sec_nos = []
for i in range(0,length,44100):
	sum=0
	k=0
	for j in range(i,i+44100):
		sum+=nos[i]
		k+=1
	sec_nos.append(sum//k)

print(nos)

print("\n\nFor Per Second now DUO\n")
sec_nos_duo = []
for i in range(0,length_duo,44100):
	sum=0
	k=0
	for j in range(i,i+44100):
		sum+=nos_duo[i]
		k+=1
	sec_nos_duo.append(sum//k)

print(nos_duo)

with open('dreams.csv',mode='w',newline='') as file:
	wrt = csv.writer(file,delimiter=',')
	#wrt.writerow([])
	for i in sec_nos:
		wrt.writerow([i])

is_plot = int(input("\n\nDo you want a plot? (0/1)\n"))
if is_plot:
	plt.plot(sec_nos)
	plt.show()
	plt.plot(sec_nos_duo)
	plt.show()

for i in range(len(nos)):
	print(int(nos[i]))