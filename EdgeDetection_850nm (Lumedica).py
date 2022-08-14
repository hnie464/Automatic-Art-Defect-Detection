# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 22:37:33 2021

@author: Hendrik
"""

import matplotlib.pyplot as plt
import numpy as np
import analysisFunctionsGallery as af
import scipy
import tifffile as tf   # External download

plt.rc('figure', max_open_warning = 0)   # Removes 20 plot limit warning   



# === HOW TO USE SCRIPT === #
#   1) Use ImageJ to sort B-scans into one C-scan (File > Import > Image Sequence...)
#   2) Import .tif (C-scan) from file location.
#   3) Select B-scan range for analysis.
#   4) Run code.

# NOTE: Variables that may need adjusting...
#       threshStrict, threshSmooth: 1310nm intensity values much smaller than 850nm, requires different max intensity percentages.
#       distance >= x, distance <= x, (Dual-Line Analysis): 1310nm resolution much smaller than 850nm, meaning smaller bumps need to be detected.



# IMPORT .TIF FILE:
im = tf.imread('D:/Honours Project/Lumedica Data/07062022_Hendrik/4 Rembrandt Scans/20220607-155040/Rembrandt_RightSideHouse (Crop).tif')

# B-SCAN RANGE: (CAUTION: Will create a plot for every B-scan in range)
start = 55   # 0 Min
finish = 511   # 511 Max



# Automatically determines threshold intensity.
#maxInt = np.amax(im)
#print(maxInt)
#threshStrict = maxInt/2.5  # 2.5 for 850nm, 1.2 for 1310nm
#threshSmooth = maxInt/3  # 6 for 850nm, 1.5 for 1310nm

# Manually set threshold intensities
threshStrict = 10000
threshSmooth = 10000



# Setting additional variables.
detected = False
x = np.arange(0,im.shape[2],1)
print('Processing...')



# === PROJECTION VIEW === #
stackedImages = np.array(())
stackedImages = np.append(stackedImages, im)

finalImage = stackedImages.reshape(int(np.sum(im.shape[0])),int(im.shape[1]),np.size(im,2))

projection = np.sum(finalImage[:,:,:],1)
plt.figure()
#plt.title('Projection View')
plt.axis('off')
plt.imshow(projection, cmap='gray')
plt.show()



# # === SURFACE & DETECTION MAPPING === #
# for n in range(start, finish + 1):  # +1 to include the end of the range in the list
#     x = x - start + 1;  # make x start at 1
#     surf1 = af.surfaceDetect(im[n,0:im.shape[1],0:im.shape[2]],thresh=threshStrict,padSize=0,scale=1,buffer=10,skip=5)   # thresh=30000
#     surf2 = af.surfaceDetect2(im[n,0:im.shape[1],0:im.shape[2]],thresh=threshSmooth,padSize=0,scale=1,buffer=10,skip=5)   # thresh=10000
#     plt.figure()
#     #plt.ylim(400)
#     plt.imshow(im[n,:,:],cmap='gray')
#     x = np.arange(0,im.shape[2],1)   # Fixes x-axis plotting issue
#     line1 = plt.plot(x,surf1,'-', color='red', linewidth=0.5)
#     line2 = plt.plot(x,surf2,'-', color='cyan', linewidth=0.5)
#     plt.title('B-Scan: n, '+ str(n))
    


# # DUAL-LINE ANALYSIS (TECHNIQUE 2)    
#     for b in range(20,492): # 0,im.shape[2]
#         distance = abs(surf1[b]-surf2[b])
#         if distance >= 15: #12 default
#             Detected = True
#             #print(distance, x[surf1[b]], surf1[b])
#             plt.plot(x[b], surf1[b], marker='+', color='cyan')
#             print('Possible point of interest detected!   B-scan #', n, '   Location:', 'x =', x[b], 'y =', surf1[b])
#             break
#         # if distance <= -12: #-12 default
#         #     Detected = True
#         #     #print(distance, x[surf1[b]], surf1[b])
#         #     plt.plot(x[b], surf1[b], marker='+', color='cyan')
#         #     print('Possible point of interest detected!   B-scan #', n, '   Location:', 'x =', x[b], 'y =', surf1[b])
#         #     break
            
    

# # PIXEL GRADIENT CHANGE (TECHNIQUE 1)
#     d_surf1=[(surf1[i+1]-surf1[i]) for i in range(len(surf1)-1)]   # localised change
      
#     for m in d_surf1:
#         if m >= 4 in d_surf1[20:im.shape[2]-20]:   # m = gradient threshold (..., -1, -2, 0, 1, 2, ...), im.shape[2]-20 removes 20px of noise from end of image
#             detected = True
#             max_value = max(d_surf1)
#             max_index = d_surf1.index(max_value)
#             if max_index in np.arange(20,im.shape[2]-20):   # ignores start and end noise
#                 plt.plot(x[max_index], surf1[max_index], marker='+', color='lightgreen')
#                 print('Possible point of interest detected!   B-scan #', n, '   Location:', 'x =', x[max_index], 'y =', surf1[max_index])
#                 break
#         elif m <= -4 in d_surf1[20:im.shape[2]-20]:
#             detected = True
#             max_value = max(d_surf1)
#             max_index = d_surf1.index(max_value)
#             if max_index in np.arange(20,im.shape[2]-20):
#                 plt.plot(x[max_index], surf1[max_index], marker='+', color='lightgreen')
#                 print('Possible point of interest detected!   B-scan #', n, '   Location:', 'x =', x[max_index], 'y =', surf1[max_index])
#                 break



# === PROJECTION MAPPING === #
tech1_detections = 0
tech2_detections = 0

plt.figure()
for i in range(start, finish + 1):
    x = x - start + 1;  # make x start at 1
    surf1 = af.surfaceDetect(im[i,0:im.shape[1],0:im.shape[2]],thresh=threshStrict,padSize=0,scale=1,buffer=10,skip=5)   # thresh=30000
    surf2 = af.surfaceDetect2(im[i,0:im.shape[1],0:im.shape[2]],thresh=threshSmooth,padSize=0,scale=1,buffer=10,skip=5)   # thresh=10000
    d_surf=[(surf1[u+1]-surf1[u]) for u in range(len(surf1)-1)]
    plt.imshow(projection, cmap='gray')
    #plt.title('Projection with Irregularities Mapped')
    plt.axis('off')
    
    
    
# DUAL-LINE ANALYSIS (TECHNIQUE 2)
    
    for b in range(20,492):
        distance = abs(surf1[b]-surf2[b])
        if distance >= 16: #12 default
            detected = True
            #print(distance, x[surf1[b]], surf1[b])
            plt.imshow(projection, cmap='gray')
            plt.plot(b, i, marker=',', color='cyan')
            tech2_detections = tech2_detections + 1
            break
        # elif distance <= -16: #-12 default
        #     detected = True
        #     #print(distance, x[surf1[b]], surf1[b])
        #     plt.imshow(projection, cmap='gray')
        #     plt.plot(b, i, marker=',', color='cyan')
        #     #count = count+1
        #     break


    
# PIXEL GRADIENT CHANGE (TECHNIQUE 1)

    d_surf1=[(surf1[i+1]-surf1[i]) for i in range(len(surf1)-1)]   # localised change

    for m in d_surf1:
        if m >= 4 in d_surf1[20:im.shape[2]-20]:   # gradient threshold (..., -1, -2, 0, 1, 2, ...)
            detected = True
            max_value = max(d_surf1)
            max_index = d_surf1.index(max_value)
            tech1_detections = tech1_detections + 1
            if max_index in np.arange(20,im.shape[2]-20):   # ignores start and end noise
                plt.plot(max_index, i, marker=',', color='lightgreen')
                break
        elif m <= -4 in d_surf1[20:im.shape[2]-20]:
            detected = True
            max_value = max(d_surf1)
            max_index = d_surf1.index(max_value)
            tech1_detections = tech1_detections + 1
            if max_index in np.arange(20,im.shape[2]-20):
                plt.plot(max_index, i, marker=',', color='lightgreen')
                break

plt.imshow(projection, cmap='gray')



# KEEP ACTIVE
print('')
print('Done!')
print('')
print('Pixel-Height Technique Detections: ', tech1_detections)
print('Dual-Line Technique Detections: ', tech2_detections)
if detected == False:
    print('Nothing of interest within the scanning range:', start, '-', finish)
    