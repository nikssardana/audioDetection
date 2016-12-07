import sys
import wave
import struct
import numpy as np

def isSilence(windowPosition):
    sumVal = sum( [ x*x for x in sound[windowPosition:windowPosition+windowSize+1] ] )
    avg = sumVal/(windowSize)
    if avg <= 0.0001:
        return True
    else:
        return False

#read from wav file
inputFile = sys.argv[1]
sound_file = wave.open(inputFile, 'r')
file_length = sound_file.getnframes()
sound = np.zeros(file_length)
for i in range(file_length):
    data = sound_file.readframes(1)
    data = struct.unpack("<h", data)
    sound[i] = int(data[0])
    #data = struct.unpack('{n}h'.format(n=file_length), data)

sound = np.divide(sound, float(2**15))
#sound is now a list of values

#detect silence and notes
i=0
windowSize = 2205
windowPosition = 0
listOfLists = []
listOfLists.append([])
maxVal = len(sound) - windowSize
while True:
    if windowPosition >= maxVal:
        break
    if not isSilence(windowPosition):
        while not isSilence(windowPosition):
            #listOfLists[i].append(sound[windowPosition:windowPosition+ windowSize+1])
            for v in sound[windowPosition:windowPosition+windowSize+1]:
                listOfLists[i].append(v)
            windowPosition += windowSize
        listOfLists.append([]) #empty list
        i += 1
    windowPosition += windowSize

frequencies = []

listOfLists.pop() #remove last empty list

#Calculating the frequency of each detected note by using DFT
for signal in listOfLists:
    w = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(w))
    l = len(signal)

    #imax = index of first peak in w
    imax = np.argsort(np.abs(w),axis=0)[-1]
    fs = freqs[imax]

    freq = abs(fs * 44100)
    frequencies.append(freq)

#print frequencies

#key-value pairs of frequencies and their corresponding names
frequenciesDict = { 27.500 : 'A0', 29.135 : 'A#0', 30.868 : 'B0', 32.703 : 'C1', 34.648 : 'C#1', 36.708 : 'D1', 38.891 : 'D#1', 41.203 : 'E1',43.654 : 'F1', 46.249 : 'F#1',48.999 : 'G1', 51.913 : 'G#1',55.000 : 'A1',58.270 : 'A#1',61.735 : 'B1',
        65.406: 'C2',  69.296: 'C#2',73.416 : 'D2',77.782:'D#2', 82.407: 'E2',87.307:'F2',92.499:'F#2',97.999 :'G2',103.826:'G#2',110.000:'A2',116.541:'A#2', 123.471: 'B2',
        130.813 : 'C3',  138.591 : 'C#3', 146.832 : 'D3', 155.564 : 'D#3', 164.814 : 'E3', 174.614 : 'F3', 184.997 :'F#3', 195.998 :'G3', 207.652 :'G#3', 220.000 : 'A3', 233.082 : 'A#3', 246.942 : 'B3',
        261.626 : 'C4',  277.183 : 'C#4', 277.183 : 'D4', 311.127 : 'D#4', 329.628 : 'E4', 349.228 : 'F4', 369.994 :'F#4', 391.995 :'G4', 415.305 :'G#4', 440.000 : 'A4', 466.164 : 'A#4', 493.883 : 'B4',
        523.251 : 'C5',  554.365 : 'C#5', 587.330 : 'D5', 622.254 : 'D#5', 659.255 : 'E5', 698.457 : 'F5', 739.989 :'F#5', 783.991 :'G5', 830.609 :'G#5', 880.000 : 'A5', 932.328 : 'A#5', 987.767 : 'B5',
        1046.502 : 'C6',  1108.731 : 'C#6', 1174.659 : 'D6', 1244.508 : 'D#6', 1318.510 : 'E6', 1396.913 : 'F6', 1479.978 :'F#6', 1567.982 :'G6', 1661.219 :'G#6', 1760.000 : 'A6', 1864.655 : 'A#6', 1975.533 : 'B6',
        2093.005 : 'C7',  2217.461 : 'C#7', 2349.318 : 'D7', 2489.016 : 'D#7', 2637.021 : 'E7', 2793.826 : 'F7', 2959.956 :'F#7', 3135.964 :'G7', 3322.438 :'G#7', 3520.000 : 'A7', 3729.310 : 'A#7', 3951.066 : 'B7',
        4186.009 : 'C8',  4434.922 : 'C#8', 4698.637 : 'D8', 4978.032 : 'D#8', 5274.042 : 'E8', 5587.652 : 'F8', 5919.912 :'F#8', 6271.928 :'G8', 6644.876 :'G#8', 7040.000 : 'A8', 7458.620 : 'A#8', 7902.133 : 'B8',
        8372.019 : 'C9',  8869.845 : 'C#9', 9397.273 : 'D9', 9956.064 : 'D#9', 10548.083 : 'E9', 11175.305 : 'F9', 11839.823 :'F#9', 12543.855 :'G9', 13289.752 :'G#9',

        }


notes = []
for num in frequencies:
    '''
    Find out the value (name) of the note from dictionary.
    If the exact key (frequency) exists, find out the value
    else find out the nearest note value
    '''
    val = frequenciesDict[num] if num in data else frequenciesDict[min(frequenciesDict.keys(), key=lambda k: abs(k-num))]
    notes.append(val)

for n in notes:
    print n,
