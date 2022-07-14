
import Convolver as cv
import readBin as rb
import BaselineCorrection as bc



if __name__ == '__main__':
    #Prompt user for file directories
    DataFolder = input("Enter directory of original data: ")
    NewFolder = input("Enter directory for the convolved data: ")

    Choice0 = input("Would you like to copy your data? (y/n) ")
    if 'y' in Choice0 or 'Y' in Choice0:
        rb.CopyContents(DataFolder,NewFolder)
    Choice1 = input("Would you like to convolve your data? (y/n) ")
    if 'y' in Choice1 or 'Y' in Choice1:
        cv.ConvolveExperiment(NewFolder)
    Choice2 = input("Would you like to baseline correct your data? (y/n) ")
    if 'y' in Choice2 or 'Y' in Choice2:
        bc.BaselineCorrect(NewFolder)
    Choice3 = input("Would you like to integrate your data automatically? (y/n) ")


