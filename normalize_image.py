import cv2
import get_image
import os
get_image.counterDirName=1
training_path='C:/Users/x/Desktop/eigen_lbph/training-data'
face_xmlFile='C:/Users/x/Desktop/eigen_lbph/opencv-files/haarcascade_frontalface_alt.xml'

class FaceDetector(object):
        def __init__ (self, xml_path):
                self.classifier= cv2.CascadeClassifier(xml_path)
        def detect(self,image,min_neighbors,min_size):                                
                # print("scale            :",scale_factor)
                # print ("neighbors       :",min_neighbors)
                # print("size             :",min_size)
                # print("scale type       :",type(scale_factor))
                biggest_only=True
                scale_factor=1.2
                flags=cv2.CASCADE_FIND_BIGGEST_OBJECT | \
                        cv2.CASCADE_DO_ROUGH_SEARCH if biggest_only else \
                        cv2.CASCADE_SCALE_IMAGE
                face_coord=self.classifier.detectMultiScale(image,scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=(min_size,min_size), flags=flags)
                return face_coord

def cut_image(image, faces_coord):
    faces=[]
    for (x,y,w,h) in faces_coord:
        w_rm= int (0.2 * w/2)
        faces.append(image[y:y+h, x+w_rm: x+ w -w_rm])
    return faces
def normalize_intensity(images):
    images_norm=[]
    for image in images:
        #print ('original size pas di filter....',image.shape)
        is_color = len(image.shape)== 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images_norm.append(cv2.equalizeHist(image))
    return images_norm

def resize(images,result_size):
    images_norm=[]
    #tunning result size
    #result_size= 100
    for image in images:
        #print ('original size',image.shape)
        height, width= image.shape[0],image.shape[1]
        width=int(result_size)
        height=int(result_size)
        dim=(width,height)
        #print ('now size',dim)
        #if image.shape <(result_size,result_size):
        resized= cv2.resize(image, (dim), interpolation=cv2.INTER_AREA)
        # else:
        #     resized=cv2.resize(image,dim,interpolation= cv2.INTER_CUBIC)
        images_norm.append(resized)
    return images_norm

def standarization(arr,resize_val,min_neighbors,min_size,path_save):
    global detector
    get_image.array_image(arr,path_save)
    dirGambar=get_image.finalDir
    #print('INI GAMBARNYA...',dirGambar)
    os.chdir(dirGambar)
    dirGambar=os.listdir()
    detector=FaceDetector(face_xmlFile)
    for image in dirGambar:
        #print("gambar kedeteksi")
        img=cv2.imread(get_image.finalDir+'/'+str(image))
        #print (training_path+'s'+str(get_image.counterDirName-1)+'/'+str(image))
        face_coord=detector.detect(img,min_neighbors,min_size)
        # cv2.imshow("nana",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #print(len(face_coord))
        if (len(face_coord)):
            #print("file on normalize process....")
            faces=cut_image(img,face_coord)
            faces=normalize_intensity(faces)
            faces= resize(faces,resize_val) 
            os.remove(get_image.finalDir+'/'+str(image))
            cv2.imwrite(get_image.finalDir+'/'+str(image),faces[0])    
        else:
                os.remove(get_image.finalDir+'/'+str(image))
                print ("no face detected, deleting file...")
    get_image.counterDirName+=1
    #print("file saved in....",training_path+'s'+str(get_image.counterDirName-1)+'/'+str(image)+'.png')
def test_image(test_image_path,resize_val,min_neighbors,min_size):
    #get data input and n  ormalize
    global face_image
    img=cv2.imread(test_image_path)
    #print (training_path+'s'+str(get_image.counterDirName-1)+'/'+str(image))
    detector=FaceDetector(face_xmlFile)
    face_coord=detector.detect(img,min_neighbors,min_size)
    if (len(face_coord)):
        #print("lalala")
        faces=cut_image(img,face_coord)
        faces=normalize_intensity(faces)
        faces=resize(faces,resize_val)    
        #cv2.imwrite(training_path+'s'+str(get_image.counterDirName-1)+'.png'+'/'+str(image),faces[0])
        face_image=faces[0]
        cv2.imshow("lala",faces[0])
        cv2.waitKey(0)
        cv2.destroyAllWindows()            

# arr=['http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_21_Pro.jpg',
#         'http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_23_Pro.jpg',
#         'http://danangmaruf.esy.es/dataAll/DANANG/WIN_20190320_04_36_25_Pro.jpg']
# path_save='C:/Users/x/Desktop/eigen_lbph/training-data2'

# standarization(arr,100,5,30,path_save)
