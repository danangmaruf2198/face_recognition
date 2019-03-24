from bs4 import BeautifulSoup
import urllib.request, urllib3, urllib.parse
import os, shutil
counterName=0

def webScrapping(url,path_save):
    global counterName,finalDir,counterDirName
    http= urllib3.PoolManager()
    response=http.request('GET',url)
    soup= BeautifulSoup(response.data)
    os.chdir(path_save)
    images= soup.find_all('a')
    #imageDirName = 's'+str(counterDirName)
    #os.mkdir(imageDirName)
    for image in images:
        link = image.get('href')
        #tergantung directory hosting
        if (link=='/dataAll/'):
            print("deleting wrong image....")
        else:
            urllib.request.urlretrieve(url+link,path_save+"/"+str(counterName)+".png")
            finalDir=path_save
            counterName += 1
    counterName=0
def array_image(arr,path_save):
    global counterName, finalDir
    #contoh array [http://danangmaruf.esy.es/dataAll/DANANG/]
    for image in arr:
        print (image)
        urllib.request.urlretrieve(image,path_save+"/"+str(counterName)+".png")
        finalDir=path_save
        counterName += 1
    counterName=0

# arr=['http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_21_Pro.jpg',
#         'http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_23_Pro.jpg',
#         'http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_25_Pro.jpg']
# path_save='C:/Users/x/Desktop/eigen_lbph/training-data'
# array_image(arr,path_save)
# url=input('masukkan directory:     ')
# webScrapping(str(url))
# webScrapping(str(url))
