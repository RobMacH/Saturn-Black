import numpy as np
import wave
import matplotlib.pyplot as plt
import pandas as pd
import os, os.path

# Open the WAV file
def fourierAnalysis(file):
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
        wav_frames = wav_file.readframes(num_frames)
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
        freq_axis = np.fft.rfftfreq(num_frames, d=1/sample_rate)

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
        return sample_rate


def main():
    directoryStr = "/home/rob-spin5/AudioMNIST/data/08"

    directory = os.fsencode(directoryStr)

    first = 1
    fileNum = 0
    fileCounter = 1

    

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            fileNum += 1
            #fourierAnalysis(directory + '/' + filename)
            continue
        else:
            continue


    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            print("Scanning file", fileCounter, "of", fileNum, end="\r")
            newSampleRate = fileChecker(directoryStr + '/' + filename)
            if(first == 1):
                oldSamepleRate = newSampleRate
                first = 0
            
            if(oldSamepleRate != newSampleRate):
                print("Different sample rates, can't compare!")
                return -1
            else:
                oldSamepleRate = newSampleRate
                fileCounter += 1

            
            continue
        else:
            continue
    
    print('\n')
        
    N = 20000
    frames = []
    axes = []
    classes = []

    fileCounter = 0
    maxAxisLength = 0
    

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            loadingBar = "\u2588" * int((fileCounter/fileNum)*100) + "\u2591" * (100 - int((fileCounter/fileNum)*100))
            print("Analysing file", fileCounter, "of", fileNum, f"|{loadingBar}|", end="\r")

            frame, axis = fourierAnalysis(directoryStr + '/' + filename)
            frames += frame
            if(len(axis) > maxAxisLength):
                maxAxisLength = len(axis)
                axes = axis

            classes += filename.split('_')[0]

            fileCounter += 1
            
            continue
        else:
            continue
    #print("after", axes)
    print('\n')
    print(frames)
    for f in range(0,len(frames)):
        #print("length of frames", len(frames[f]))
        frames[f][:] = frames[f][0:maxAxisLength]


    

    df = pd.DataFrame(data=frames, columns=axes)
    print("\nDone...")

    print(df)

    print(f"Data frame head: {df.head()}")

    

    


if __name__ == "__main__":
    main()