import cv2
import numpy as np
#import HOG

import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, color, exposure

def HOGCalculat(template):
    hog_computer = cv2.HOGDescriptor()
    a = hog_computer.compute(template)
    return a

def hogg(image):
        #image = color.rgb2gray(image)
        fd, hog_image = hog(image, orientations=6, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualize=True)
        #hog_image_rescaled = exposure.rescale_intensity(hog_image,in_range=(0,0.02))
        #cv2.imshow("Hogwarts", hog_image_rescaled)
        return hog_image

def initVariable(dh, dw, hh, ww, h,w, dif):
    if (dw-dif)<=0:
        debutx=0
    else:
        debutx = dw-dif
        
    if (dh-dif)<=0:
        debuty=0
    else:
        debuty = dh-dif
        
    if (dw + ww + dif)> w:
        finx = w
    else:
        finx = dw + ww + dif
        
    if (dh + hh + dif)>h:
        finy = h
    else:
        finy =dh + hh + dif
    #print(debutx, debuty , finx, finy)
    return debutx, debuty , finx, finy



def compare1(template, org, original, dh, dw, summ):
    orgg = original.copy()
    hh, ww = template.shape
    h,w = org.shape
    #25 pixels
    debutx, debuty , finx, finy = initVariable(dh, dw, hh, ww, h,w, dif = 25)
    poop = np.sum(template)*10
    
    for o in range(debuty,finy,1):
        for oo in range(debutx,finx,1):
            partie = org[o:hh+o, oo:ww+oo]
            res = np.abs(np.subtract(partie,template))
            kk = np.sum(res)
            #print("somme elm resultat, min somme",kk, poop)
            if kk < poop:
                poop = kk
                posh, posw = o, oo
                #print(o,oo, kk)
            if ww+oo>= w:
                break
        if hh+o >= h:
             break
    cv2.rectangle(orgg, (posw-20, posh-10 ), ( posw+ww-10, posh+hh), (0,255,255), 2)
    tem = org[posh:posh+hh, posw:posw+ww]
    temm = original[posh:posh+hh, posw:posw+ww]
    
    #temm = cv2.cvtColor(temm, cv2.COLOR_BGR2GRAY)
    #temm = hogg(temm)
    
    q = np.abs(np.subtract(tem,template))
    re = np.sum(q)
    #print("saus template et temp, summ", re, summ)
    #print("saus template et temp", re)
    #print("summ envoyé", summ)
    if  re<= summ:
        #print("changement du summ: ", summ)
        template = temm
        summ = re
        #print("deviens: ", summ)
  
    if (re > 280):
        template = temm
        summ = re
        #print("changement du summ devient: ", summ)
    else:
        template = originale[dh:dh+hh, dw:dw+ww]
    return posh, posw, orgg, template, summ

    

def main():
    img=[]
    dh, dw = 125,208
    #template
    t = cv2.imread("1.jpg")

   
    for i in range(1, 600, 3):
        if(i<10):
            k = "0000000"
        elif(i<100):
            k = "000000"
        else:
            k = "00000"
        img_bgr = cv2.imread(k+str(i)+".jpg")
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        img1 = img_bgr.copy()
        hog2 = hogg(img_gray)
        
        t = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
        hog1 = hogg(t)
        
        if i == 1:
            #print(hog1.shape, t.shape, hog2.shape, img_bgr.shape)
            dh, dw, aff, t, st = compare1(template = hog1 , org = hog2, original = img_bgr, dh=dh, dw=dw, summ =15000)
            
            #print(st)
            #print(dh, dw, aff, t, summ)
            #cv2.imshow("resultat", aff)
            #cv2.waitKey(0)
            img.append(aff)
        #print("nouveau depart", dh, dw)
        else :
            dh, dw, aff, t, st = compare1(template = t , org = hog2, original = img_bgr, dh=dh, dw=dw, summ= st)
            img.append(aff)
            #cv2.imshow("resultat", aff)
            #cv2.waitKey(0)
    return img


    
#main()
    
import time
im = main()

print("DEBUT DE LA VIDEO")
# Read until video is completed
for a in im:
    cv2.imshow('Frame',a)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    k = cv2.waitKey(30) & 0xff
    if k == ord('s'):
        refaire(im)
    time.sleep(0.2)


 



      
