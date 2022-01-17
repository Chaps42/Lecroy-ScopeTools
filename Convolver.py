import readBin as rb
import numpy as np
import os
from shutil import copyfile
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #Prompt user for file directories
    DataFolder = input("Enter directory of original data: ")
    NewFolder = input("Enter directory for the convolved data: ")

    #Read Data Folder and return info about the datasets
    Allnames = os.listdir(DataFolder)
    sub = ['.spectra','.DS_Store','.h5']
    for i in range(len(sub)):
        for text in Allnames:
            if sub[i] in text:
                Allnames.remove(text)
    ChannelNames = []
    FileName = []
    FileNumber = []
    trim1 = []
    trim2 = []
    for i in range(len(Allnames)):
        trim1 = ''
        trim2 = ''
        ChannelNames.append(Allnames[i][0:2])
        FileNumber.append(Allnames[i][-9:-4])
        trim1 = Allnames[i][:-9]
        trim2 = trim1[2:]
        FileName.append(trim2)
    Channels = list(set(ChannelNames))
    Names = list(set(FileName))
    Numbers = list(set(FileNumber))
    Numbers.sort()
    Another = 'y'
    while Another =='y':
        if Another == 'y':
            #Prompt user for test spectra
            print()
            print("File code: ", Names)
            print("Available channels: ", Channels)
            print("Spectrum numbers: " ,min(Numbers),'-',max(Numbers))
            Channel = input("Which channel would you like to convolve? (choose from above): ")
            TestNum = input("Which spectra would you like to test convolution? (ex. '00001'): ")
            Channels.remove(Channel)
            
            #Copy File to New Folder
            name = Channel + Names[0] + TestNum+'.trc'
            copyfile(DataFolder+'/'+name,NewFolder+'/'+name)

            #Read Data and Convolve
            Convolution = input("Convolve as Gaussian 'G' or Boxcar 'B'?: ")
            PointWidth = int(input("Enter the width in data points of convolution (int): "))
            DataIn = rb.readBin(NewFolder,name)
            x,y = rb.Convolution(DataIn[0,:],DataIn[1,:],Convolution,PointWidth)

            plt.plot(DataIn[0,:],DataIn[1,:])
            plt.plot(x,y)
            plt.title(name+ ' Convolved with '+Convolution+', '+str(PointWidth)+' points wide')
            plt.legend(['Unconvolved Data' ,' Convolved Data'])
            plt.show()

            Another = input("Would you like to convolve a another file? (y/n): ")
            Channels.append(Channel)

    #Asks if you want to convolve all data files
    ConvAll = input("Would you like to convolve all "+Channel+" files with this setup? (y/n): ")
    if ConvAll == 'y':

    #Convolving and Copying all files
        for i in range(len(Numbers)):
            #Copying unconvolved data
            for j in range(len(Channels)):
                name = Channels[j] + Names[0] + Numbers[i] + '.trc'
                copyfile(DataFolder+'/'+name,NewFolder+'/'+name)

            #Copying Convolved Data
            name = Channel + Names[0] + Numbers[i] + '.trc'
            copyfile(DataFolder+'/'+name,NewFolder+'/'+name)
            DataIn = rb.readBin(NewFolder,name)
            x,y = rb.Convolution(DataIn[0,:],DataIn[1,:],Convolution,PointWidth)

            rb.OverrideData(y,NewFolder,name)
            if i%5 ==0:
                print("Progress: ",i,"/",len(Numbers),'...')
        
    print("Finished!")

        
        
        

        

    
