# audioDetection

A Python Script to Find out the Notes in a .wav file.

# Usage
python final.py <filename>
Ex: python final.py sampleAudio/Audio_1.wav

# Requirements:
1. Numpy (http://www.numpy.org/)
2. Wave (https://docs.python.org/2/library/wave.html)

# Other modules

1. Sys (https://docs.python.org/2/library/sys.html)
2. Struct (https://docs.python.org/2/library/struct.html)

# Description

The script takes a .wav file as input and calculates the frequencies.

=>The wav file is assumed to be consisting of discrete notes separated by silence.

=>The values in wav file are read using wave module into a sound array.

=>It then detects the silence in the file by using a working window of fixed size, say 2205. The window is slided over the array.

=>If average sum of squares of values in the window is less than a threshold value, say 0.0001, it is considered as silence.

=>Various notes is thus obtained in the variable listOfLists.

=>The discrete cosine transform (DCT) is then calculated using Fast Fourier Transform function numpy.fft.fft().

=>This DCT value is then used to calculate the frequency of note.

=>The frequency is then mapped to the nearest known note and the values are then displayed.
