import numpy as np
import wave
import matplotlib.pyplot as plt
import pandas as pd
import os, os.path
import math

# Open the WAV file
def fourierAnalysis(file, maxFrameNum):
    with wave.open(file, 'rb') as wav_file:
        #print("Scanning file: ", file)
        # Get the number of frames, channels and sample rate
        num_frames = wav_file.getnframes()
        #print("Number of frames: ", num_frames)
        num_channels = wav_file.getnchannels()
        #print("Number of channels: ", num_channels)
        sample_rate = wav_file.getframerate()
        #print("Sample rate: ", sample_rate)
        
        # Read the audio frames

        padding = (maxFrameNum - num_frames)

        if(padding % 2 != 0):
            # is odd
            padding += 1
            

        leftPadding = math.ceil(padding/2)
        rightPadding = math.floor(padding/2)
        wav_frames = wav_file.readframes(num_frames)
        #print("frames", num_frames,"wave frames:", len(wav_frames))
        wav_frames += b'00' * (rightPadding)
        wav_frames = (b'00' * leftPadding) + wav_frames
        #print("frames", num_frames,"wave frames:", len(wav_frames))
        wav_frames = np.frombuffer(wav_frames, dtype=np.int16)
        
        # Apply FFT to each channel
        fft_frames = []
        for channel in range(num_channels):
            # Get the channel data
            channel_data = wav_frames[channel::num_channels]
            # Apply FFT on the channel data
            fft_data = np.fft.rfft(channel_data)
            fft_frames.append(abs(fft_data.real))
        
        # Get the frequency axis
        freq_axis = np.fft.rfftfreq(int(len(wav_frames)), d=1/(2048))

    return fft_frames, freq_axis

        
    # The FFT frames contain the frequency spectra for each channel
    #print(fft_frames)

def fileChecker(file):
    with wave.open(file, 'rb') as wav_file:
        ##print("Scanning file: ", file)
        # Get the number of frames, channels and sample rate
        num_frames = wav_file.getnframes()
        #print("Number of frames: ", num_frames)
        num_channels = wav_file.getnchannels()
        #print("Number of channels: ", num_channels)
        sample_rate = wav_file.getframerate()
        return num_frames, num_channels, sample_rate


def makeDataSet(directoryStr):
    if(directoryStr == None):
        directoryStr = "/home/rob-spin5/AudioMNIST/data/08"

    directory = os.fsencode(directoryStr)

    first = 1
    fileNum = 0
    fileCounter = 1

    f = open("axes_values.txt", 'w')

    

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            fileNum += 1
            #fourierAnalysis(directory + '/' + filename)
            continue
        else:
            continue

    minFrameNum = 99999
    maxFrameNum = 0

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            print("Scanning file", fileCounter, "of", fileNum, end="\r")
            frame_num, channels, newSampleRate = fileChecker(directoryStr + '/' + filename)
            if(first == 1):
                oldSamepleRate = newSampleRate
                first = 0
            
            if(oldSamepleRate != newSampleRate):
                print("Different sample rates, can't compare!")
                return -1
            else:
                oldSamepleRate = newSampleRate

            if(frame_num > maxFrameNum):
                maxFrameNum = frame_num    
            
            if(frame_num < minFrameNum):
                minFrameNum = frame_num

            fileCounter += 1

            
            continue
        else:
            continue
    
    print('\n')

    #print("Minimum Frame Count:", minFrameNum)
    #print("Maximum Frame Count:", maxFrameNum)
        
    N = 20000
    frames = []
    circumFrames = []
    axes = []
    classes = []

    fileCounter = 1
    minAxisLength = 99999999
    maxAxisLength = 0
    

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            loadingBar = "\u2588" * int((fileCounter/fileNum)*100) + "\u2591" * (100 - int((fileCounter/fileNum)*100))
            print("Analysing file", fileCounter, "of", fileNum, f"|{loadingBar}|", end="\r")

            frame, axis = fourierAnalysis(directoryStr + '/' + filename, maxFrameNum)
            f.write(np.array2string(axis) + f"length: {len(axis)}" + '\n')
            frames += frame
            if(len(axis) < minAxisLength):
                #print("\n Min:", minAxisLength)
                minAxisLength = len(axis)
                axes = axis
            
            if(len(axis) > maxAxisLength):
                maxAxisLength = len(axis)

            classes += filename.split('_')[0]

            fileCounter += 1
            
            continue
        else:
            continue
    #print(f"Max Axis Length: {maxAxisLength} | Min Axis Length: {minAxisLength}")
    f.close
    for f in range(0,len(frames)):
        #print("length of frames", len(frames[f]))
        circumFrames.insert(0, frames[f][:minAxisLength])

    print("Creating dataframe...")
    df = pd.DataFrame(data=frames, columns=axes)

    df.insert(0, 'class', classes, True)

    print("\nDone...")

    return df
    


if __name__ == "__main__":
    makeDataSet("/home/rob-spin5/AudioMNIST/data/08")