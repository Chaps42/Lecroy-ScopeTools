import pybaselines as pb
import numpy as np
import matplotlib.pyplot as plt
import os
from shutil import copyfile
import readBin as rb
    

def BaselineCorrect(NewFolder):
    Channels,Names,Numbers = rb.getNameList(NewFolder)
    Another = 'y'
    while Another =='y':
        #Prompt user for test spectra
        print()
        print("File code: ", Names)
        print("Available channels: ", Channels)
        print("Spectrum numbers: " ,min(Numbers),'-',max(Numbers))
        Channel = input("Which channel would you like to correct? (choose from above): ")
        TestNum = input("Which spectra would you like to test baseline correction? (ex. '00001'): ")
        
        #Copy File to New Folder
        name = Channel + Names[0] + TestNum+'.trc'

        #Read Data and Convolve
        knots = int(input("How many knots do you want to model the baseline with?: "))
        DataIn = rb.readBin(NewFolder,name)
        y,weights = pb.spline.mixture_model(DataIn[1,:],num_knots = knots)

        plt.plot(DataIn[0,:],DataIn[1,:])
        plt.plot(DataIn[0,:],y)
        plt.title(name+ ' modeled with '+str(knots)+'knots')
        plt.legend(['Data' ,'Calculated Baseline'])
        plt.show()


        plt.plot(DataIn[0,:],DataIn[1,:]-y+.0005)
        plt.title(name+ 'Baseline subtracted')
        plt.show()

        Another = input("Would you like to baseline correct a another file? (y/n): ")

        #Asks if you want to convolve all data files
    ConvAll = input("Would you like to correct all baselines for channel "+Channel+" with this setup? (y/n): ")
    if ConvAll == 'y':

    #Convolving all files
        for i in range(len(Numbers)):
            #Copying Convolved Data
            name = Channel + Names[0] + Numbers[i] + '.trc'
            DataIn = rb.readBin(NewFolder,name)
            y,weights = pb.spline.mixture_model(DataIn[1,:],num_knots = knots)

            rb.OverrideData(DataIn[1,:]-y+.0005,NewFolder,name)
            if i%5 ==0:
                print("Progress: ",i,"/",len(Numbers),'...')
            
        print("Finished!")