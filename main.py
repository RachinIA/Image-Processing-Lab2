import cv2
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import tkinter as tk

### Comparison in % ###

def PSNR(im1, im2):
    mse = np.mean((im1 - im2) ** 2)
    if (mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def fileOpen():
    ###Choose image on local machin###
    fIn=tk.filedialog.askopenfilename(title="Select image", filetypes=[("Image",["jpg", "*.jpg", "*.png", "*.jpeg"])])
    if(fIn):  ##Success
        return fIn
    else:  ##Fail
        return -1

###Max/Min limit###
def clamp(val, max, min):
    if(val <= min):
        return min
    elif(val >= max):
        return max
    else:
        return val

### Salt & Pepper Niose###
def spFilter(image,koef):
    result = np.zeros(image.shape,np.uint8)
    secondKoef = 1 - koef 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rand = random.random()
            if rand < koef:
                result[i][j] = 0
            elif rand > secondKoef:
                result[i][j] = 255
            else:
                result[i][j] = image[i][j]
    return result

### Median Filter ###
def medianFilter(imageOrig):
    image=imageOrig
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rad = 3
            n = rad*rad
            radius = rad//2
            arrR=[]
            arrG=[]
            arrB=[]
            for k in range(n):
                arrR.append(0)
                arrG.append(0)
                arrB.append(0)
            k=0
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    ix = clamp(i+x,image.shape[0]-1,0)
                    jy = clamp(j+y,image.shape[1]-1,0)
                    (b, g, r) = image[ix,jy]
                    arrR[k]=r
                    arrG[k]=g
                    arrB[k]=b
                    k+=1
            arrR.sort()
            arrG.sort()
            arrB.sort()
            image[i,j] = (arrB[n//2],arrG[n//2],arrR[n//2])
    return image

### Average Filter ###
def averageFilter(imageOrig):
    image=imageOrig
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rad = 5
            n = rad*rad
            radius = rad//2
            mR=0
            mG=0
            mB=0
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    ix = clamp(i+x,image.shape[0]-1,0)
                    jy = clamp(j+y,image.shape[1]-1,0)
                    (b, g, r) = image[ix,jy]
                    mR+=r
                    mG+=g
                    mB+=b
            image[i,j] = (mB//n,mG//n,mR//n)
    return image

### Visual tilters test ###
def visualTestFilters():
    file = fileOpen()
    if (file == -1):
        sys.exit()
    image = cv2.imread(file)
    cv2.imshow("Image", image)
    sp = spFilter(image, 0.1)
    cv2.imshow("Salt & Pepper", sp)
    median = medianFilter(sp)
    cv2.imshow("s&pAfterMedianFilter", median)
    average = averageFilter(sp)
    cv2.imshow("s&pAfterAverageFilter", average)
    medianCV = cv2.medianBlur(sp, 3)
    cv2.imshow("s&pAfterCVMedianFilter", medianCV)
    cv2.waitKey(0)  #Uncomment to wait key befor closing image
    cv2.destroyAllWindows()  #Uncomment to close all the windows
##############

### Comparison in time ###
def compareMineVsCV():
    file = fileOpen()
    if (file == -1):
        sys.exit()
    image = cv2.imread(file)
    ################################
    """Create window with results"""
    windowResults = tk.Toplevel(root)
    lbMy=tk.Label(windowResults, text="||\n||\n||\n||\n||").grid(row = 0, column = 1,rowspan = 5)
    lbMy=tk.Label(windowResults, text="Time").grid(row = 0, column = 2)
    lbMy=tk.Label(windowResults, text="||\n||\n||\n||\n||").grid(row = 0, column = 3,rowspan = 5)
    lbMy=tk.Label(windowResults, text="Similarity").grid(row = 0, column = 4)
    lbMy=tk.Label(windowResults, text="Salt & Pepper realization").grid(row = 1, column = 0)
    lbMy=tk.Label(windowResults, text="Median realization").grid(row = 2, column = 0)
    lbCV=tk.Label(windowResults, text="Average realization").grid(row = 3, column = 0)
    lbCV=tk.Label(windowResults, text="CV median realization").grid(row = 4, column = 0)
    ############################
    ### Salt & Pepper ###
    startTime = time.time()
    sp = spFilter(image, 0.1)
    myResultTimeSP = time.time() - startTime
    mySPSimilarity = PSNR(image, sp)
    #############
    ### CV median ###
    startTime = time.time()
    medianCV = cv2.medianBlur(sp, 3)
    cvResultTime= time.time() - startTime
    cvMedianSimilarity = PSNR(image, medianCV)
    ###############
    ### Median ###
    startTime = time.time()
    median = medianFilter(image)
    myResultTimeMedian = time.time() - startTime
    myMedianSimilarity = PSNR(medianCV, median)
    #############
    ### Average ###
    startTime = time.time()
    average = averageFilter(image)
    myResultTimeAverage = time.time() - startTime
    myAverageSimilarity = PSNR(medianCV, average)
    #############
    ################################
    """Change window with results"""
    lbMy=tk.Label(windowResults, text=str(round(myResultTimeSP,4))).grid(row = 1, column = 2)
    lbMy=tk.Label(windowResults, text=str(mySPSimilarity)+' %').grid(row = 1, column = 4)
    lbMy=tk.Label(windowResults, text=str(round(myResultTimeMedian,4))).grid(row = 2, column = 2)
    lbMy=tk.Label(windowResults, text=str(myMedianSimilarity)+' %').grid(row = 2, column = 4)
    lbMy=tk.Label(windowResults, text=str(round(myResultTimeAverage,4))).grid(row = 3, column = 2)
    lbMy=tk.Label(windowResults, text=str(myAverageSimilarity)+' %').grid(row = 3, column = 4)
    lbMy=tk.Label(windowResults, text=str(round(cvResultTime,4))).grid(row = 4, column = 2)
    lbMy=tk.Label(windowResults, text=str(cvMedianSimilarity)+' %').grid(row = 4, column = 4)
    ################################

######################
"""Buttons and form"""
######################
root = tk.Tk()
hsvBut1 = tk.Button(root, text = 'Visual test of filters', activebackground = "#555555", command = visualTestFilters).grid(row = 0, column = 0)
hsvBut2 = tk.Button(root, text = 'Comparison of my and cv realization', activebackground = "#555555", command = compareMineVsCV).grid(row = 0, column = 2)
lbFreeSpace = tk.Label(root, text = '||').grid(row = 0, column = 1)
root.mainloop()
######################
