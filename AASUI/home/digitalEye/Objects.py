import cv2
import os

#Always path in packeage form pacakge not relative
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

frontFaceCascade='xmldata/haarcascade_frontalface_default.xml'
smileFaceCasecade='xmldata/haarcascade_smile.xml'

class Face:
      'Extracting Face From Image'
      def __init__(self,scaleFactor=1.2,minNeighbors=5,minh=80,minw=80):
          self.scaleFactor=scaleFactor
          self.minNeighbors=minNeighbors
          self.minh=minh
          self.minw=minw

      def getData(self,image,cascadeObj):
          gimage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
          faces = cascadeObj.detectMultiScale(gimage,self.scaleFactor,self.minNeighbors,minSize=(self.minh,self.minw)) #check
          faceImages=[]
          for (x,y,w,h) in faces:
              #crop image -> cropImage=image[y:y+w,x:x+h]
              cropImage=image[y:y+w,x:x+h]
              faceImages.append(cropImage)

          return faceImages    #  NOTE: return oringinal face not gray

      def  getFaces(self,image): #return faces image list from image
          faceObj=cv2.CascadeClassifier(os.path.join(__location__, frontFaceCascade))
          return self.getData(image,faceObj)
