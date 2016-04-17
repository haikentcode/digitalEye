from digitalEye import Objects as obj
from digitalEye import Recog as rec
import sys
import cv2
import os

def hkresize(image):
    x=image.shape[1]
    if x >=1000:
            r=400.0/x
            dim=(400,int(image.shape[0]*r))
            resize=cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
            return resize
    return image

def testObjects():
    image=raw_input("ImagePath:")
    face=obj.Face(1.2,1,20,20)
    img=cv2.imread(image)
    img=hkresize(img)
    faces=face.getFaces(img)
    print "find faces=",len(faces)
    i=0
    for image in faces:
      cv2.imshow(str(i)+".jpg",image)
      i+=1
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def fileIsImage(file):
    imageEx=("jpg","png","JPG","jpeg","JPEG","PNG")
    if file.endswith(imageEx):
        return True
    else:
        return False

def getImagesLables(dirPath):
    images=[]
    lables=[]
    for name in os.listdir(dirPath):
        try:
            path=os.path.join(dirPath,name)
            if os.path.isfile(path):
                if fileIsImage(path):
                   img=cv2.imread(path)
                   img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                   img=resize=cv2.resize(img,(300,300),interpolation=cv2.INTER_AREA)
                   images.append(img)
                   lables.append(int(name.split(".")[0]))
        except:
                print "error in scanDir"
    return images,lables


def testRecog():
        images,lables=getImagesLables("./data/")
        recog = rec.Recognizer()
        recog1 = rec.Recognizer()
        recog2 = rec.Recognizer()
        recog.train(images,lables,0)
        recog1.train(images,lables,1)
        recog2.train(images,lables,2)

        face=obj.Face(1.9,3,20,20)
        cap=cv2.VideoCapture("http://10.42.0.41:8080/video") #   cap=cv2.VideoCapture(0) #
        hk=True
        print cap
        while(hk):
           ret,frame=cap.read()
           cv2.imshow('frame',frame)
           faces=face.getFaces(frame)
           print "faces Found:",len(faces)
           for f in faces:
                simg=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
                simg=cv2.resize(simg,(300,300),interpolation=cv2.INTER_AREA)
                a=recog.getLable(simg)
                b=recog1.getLable(simg)
                c=recog2.getLable(simg)
                print "predictedLable:",a,b,c

           if cv2.waitKey(1)& 0xFF==ord('q'):
                 break
        cv2.destroyAllWindows()


def testRecogWithImage():
    images,lables=getImagesLables("./data/")
    recog = rec.Recognizer()
    recog1 = rec.Recognizer()
    recog2 = rec.Recognizer()
    recog.train(images,lables,0)
    recog1.train(images,lables,1)
    recog2.train(images,lables,2)
    face=obj.Face(1.9,3,20,20)
    image=raw_input("ImagePath:")
    img=cv2.imread(image)
    faces=face.getFaces(img)
    print "find faces=",len(faces)
    for image in faces:
      simg=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      simg=cv2.resize(simg,(300,300),interpolation=cv2.INTER_AREA)
      a=recog.getLable(simg)
      b=recog1.getLable(simg)
      c=recog2.getLable(simg)
      print a,b,c
      if a[1] < 100:
           cv2.imshow(str(a[0])+":"+str(a[1])+".jpg",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    if __name__ == "__main__":
      funcList=[testObjects,testRecog,testRecogWithImage]
      if len(sys.argv) > 1:
          test=sys.argv[1]
          for func in funcList:
                       if func.func_name == test :
                             func()
