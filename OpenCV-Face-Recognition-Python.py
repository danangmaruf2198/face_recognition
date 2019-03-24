import cv2
import os,shutil
import numpy as np
import urllib.request, urllib3, urllib.parse
from bs4 import BeautifulSoup
import normalize_image
import get_image
from tkinter import *
import time
import PIL 
from multiprocessing import Process, Lock, Value, Array

eig_conf,lbph_conf=0,0
url='http://danangmaruf.esy.es/dataAll/DANANG/'
test_image_path='C:/Users/x/Desktop/eigen_lbph/test-data/danang.jpg'
arr=['http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_21_Pro.jpg',
        'http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_23_Pro.jpg',
        'http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_25_Pro.jpg']

#training path untuk lbph
training_path='C:/Users/x/Desktop/eigen_lbph/training-data'
#training path untuk eigen
training_path2='C:/Users/x/Desktop/eigen_lbph/training-data2'
def collect_dataset(counterName,path):
    images,labels=[],[]
    labels_dic={}
    for image in os.listdir(path):
        #print(image)
        images.append(cv2.imread(path+'/'+image,0))
        #cv2.imshow("lolo",cv2.imread(get_image.training_path+'s'+str(counterDirName-1)+'/'+image,0))
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        labels.append(0)
    return(images,np.array(labels),labels_dic)
def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)
    label, confidence = face_recognizer.predict(face)
    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5) 
    return img
def loop_a(lbph_conf,array):
    counter=10
    normalize_image.standarization(arr,200,6,30,training_path)
    image,labels,label_dic=collect_dataset(0,training_path)#data training
    normalize_image.test_image(test_image_path,200,6,30,)
    os.chdir(training_path)
    for i in os.listdir():
        shutil.copy(i,training_path+'/'+str(counter)+'.png')
        counter+=1
    face_image=normalize_image.face_image
    rec_lbph = cv2.face.LBPHFaceRecognizer_create()
    rec_lbph.train(image,labels)
    #label,conf=rec_fisher.predict(face_image)
    lable,conf=rec_lbph.predict(face_image)
    lbph_conf.value=conf
    print ('lbph conf   :',lbph_conf.value)
    os.chdir(training_path)
    for i in os.listdir():
        os.remove(i)
    

def loop_b(eig_conf,array):
    normalize_image.standarization(arr,30,5,30,training_path2)
    image2,labels2,label_dic2=collect_dataset(0,training_path2)#data training
    normalize_image.test_image(test_image_path,30,5,30)
    face_image2=normalize_image.face_image
    rec_eig= cv2.face.EigenFaceRecognizer_create()
    rec_eig.train(image2,labels2)
    label,conf=rec_eig.predict(face_image2)
    eig_conf.value=conf
    print ('eigen conf  :',eig_conf.value)
    os.chdir(training_path2)
    for i in   os.listdir():
        os.remove(i)
if __name__ == '__main__':
    lock=Lock()
    num = Value('d', 0.0)
    num2= Value('d',0.0)
    array = Array('i', range(10))
    lbph=Process(target=loop_a,args=(num2,array))
    lbph.daemon= True
    eigen=Process(target=loop_b,args=(num,array))
    eigen.daemon=False
    lbph.start()
    time.sleep(1)
    eigen.start()
    lbph.join()
    eigen.join()
    total_conf=((num.value/10)+num2.value)/2
    print("total conf   :",total_conf)
