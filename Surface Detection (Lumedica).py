# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 22:43:46 2022

@author: Hendrik
"""

import matplotlib.pyplot as plt
import numpy as np
import analysisFunctionsGallery as af   # Separate Python file
import scipy
import tifffile as tf   # Separate anaconda download (Install through anaconda terminal)

plt.rc('figure', max_open_warning = 0)   # Removes 20 plot limit warning   



# === HOW TO USE SCRIPT === #
#   1) Use ImageJ to sort B-scans into one C-scan (File > Import > Image Sequence...)
#   2) Import .tif (C-scan) from file location.
#   3) Select B-scan range for analysis.
#   4) Run code.

# NOTE: Variables that may need adjusting:
#       thresh - the threshold intensity for the surface line (between 0-255).



# IMPORT .TIF FILE:
im = tf.imread('D:/Honours Project/Lumedica Data/07062022_Hendrik/20220607-160422/Rembrandt_Bottom.tif')

# B-SCAN RANGE: (CAUTION: Will create a plot for every B-scan in range)
start = 100   # 0 Min
finish = 105   # 1024 Max (B-scans are duplicated, should really be max 512)

# Threshold intensity for surface mapping.
thresh = 100   # Surface line threshold



# Setting additional variables.
x = np.arange(0,im.shape[2],1)
print('Processing...')



# === PROJECTION VIEW (EN-FACE) === #
stackedImages = np.array(())   # Creates an empty array
stackedImages = np.append(stackedImages, im)   # Appends the intensity values of the C-scan into array
finalImage = stackedImages.reshape(int(np.sum(im.shape[0])),int(im.shape[1]),np.size(im,2))   # Reshapes the image array
projection = np.sum(finalImage[:,:,:],1)   # Converts the 3D image into a 2D projection image
plt.figure()
plt.axis('off')
plt.imshow(projection, cmap='gray')
plt.show()



# === SURFACE LINE PLOTTING === #
for n in range(start, finish + 1):  # +1 to include the end of the range in the list
    x = x - start + 1;  # make x start at 1
    surf = af.surfaceDetect(im[n,0:im.shape[1],0:im.shape[2]],thresh=thresh,padSize=0,scale=1,buffer=10,skip=5)   # Determines surface line using analysisFunctionsGallery.py
    #surf2 = af.surfaceDetect2(im[n,0:im.shape[1],0:im.shape[2]],thresh=thresh,padSize=0,scale=1,buffer=10,skip=5)   # Another smoother surface line
    plt.figure()
    plt.imshow(im[n,:,:],cmap='gray')
    x = np.arange(0,im.shape[2],1)   # Fixes x-axis plotting issue
    line = plt.plot(x,surf,'-', color='red', linewidth=0.5)   # Plots red surface line (strict)
    #line2 = plt.plot(x,surf2,'-', color='blue', linewidth=0.5)   # Plots blue surface line (smooth)
    plt.title('B-Scan: n, '+ str(n))
    plt.ylim([1024,0])
    plt.show()