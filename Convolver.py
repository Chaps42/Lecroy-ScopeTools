import readBin as rb
import numpy as np
import os
from shutil import copyfile
import matplotlib.pyplot as plt
from statistics import mode
import scipy.signal as signal
        
def ConvolveDataset(x,y,Type,points):
    delta = x[1]-x[0]
    DeltaT = x[-1]-x[0]
    
    Boxcar = lambda  X: 1 if (X <= points*delta/2 and X>= -points*delta/2) else 0
    Gaussian = lambda X: np.e**(-.5*(X)**2/(delta*points)**2)
    
    xc = np.arange(-5*points*delta,5*points*delta,delta)
    yc = np.zeros(len(xc))

    if Type == 'B':
        for i in range(len(yc)):
            yc[i] = Boxcar(xc[i])
    elif Type == 'G':
        for i in range(len(yc)):
            yc[i] = Gaussian(xc[i])
    else:
        return

    yc = yc/np.trapz(yc,xc) #Area of Convolve = 1
    Convolve = signal.convolve(y,yc,mode = 'same')*delta

    return x,Convolve 

def ConvolveExperiment(NewFolder):
    Channels,Names,Numbers = rb.getNameList(NewFolder)
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

            #Read Data and Convolve
            Convolution = input("Convolve as Gaussian 'G' or Boxcar 'B'?: ")
            PointWidth = int(input("Enter the width in data points of convolution (int): "))
            DataIn = rb.readBin(NewFolder,name)
            x,y = ConvolveDataset(DataIn[0,:],DataIn[1,:],Convolution,PointWidth)

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

    #Convolving all files
        for i in range(len(Numbers)):
            #Copying Convolved Data
            name = Channel + Names[0] + Numbers[i] + '.trc'
            DataIn = rb.readBin(NewFolder,name)
            x,y = ConvolveDataset(DataIn[0,:],DataIn[1,:],Convolution,PointWidth)

            rb.OverrideData(y,NewFolder,name)
            if i%5 ==0:
                print("Progress: ",i,"/",len(Numbers),'...')
        
    print("Finished!")
        

    
if __name__ == '__main__':
    #Prompt user for file directories
    DataFolder = input("Enter directory of original data: ")
    NewFolder = input("Enter directory for the convolved data: ")

    ConvolveExperiment(DataFolder,NewFolder)
        