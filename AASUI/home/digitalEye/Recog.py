
import numpy as np
import cv2

class Recognizer:
     def __init__(self):
         self.images=[]
         self.lables=np.array([])

     def train(self,images,lables,recogType=0):
           self.images = images
           self.lables = np.array(lables)
           'arg=recogType:[createLBPHFaceRecognizer,createFisherFaceRecognizer,createEigenFaceRecognizer]'
           recogs=[cv2.createLBPHFaceRecognizer,cv2.createFisherFaceRecognizer,cv2.createEigenFaceRecognizer]
           self.recognizer = recogs[recogType]()
           self.recognizer.train(self.images,self.lables)

     def  getLable(self,sampleImage): # image is gray
             predictedLable , conf = self.recognizer.predict(sampleImage)
             return predictedLable , conf
