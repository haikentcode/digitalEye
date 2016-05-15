from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect
from django.contrib import auth
from home.models import  Teacher , Attendance , Student ,Log ,ImageData

from digitalEye import Objects as obj
from digitalEye import Recog as rec
import sys
import cv2
import os
import datetime
import time
from django.views.decorators.csrf import csrf_exempt


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def rhome(request):
    return HttpResponseRedirect('/home/')
def cpath(fpath):
    return os.path.join(__location__, fpath)
def onTeacher(request):
      if request.session.get('teacher'):
         return Teacher.objects.get(emailId=request.session.get('teacher'))
      else:
         return None

def getStudent(rollNumber):
    return Student.objects.get(rollNumber=rollNumber)

def index(request):
    if request.session.get('teacher',None):
        unsetBranchCourseBatch(request)
        teacher=onTeacher(request)
        return render(request,'home/home.html',{"user":teacher,'range':range(2010,2222)})
    else:

       return HttpResponseRedirect('/login/')



def login(request):
    error=""
    if request.POST:
     data=request.POST
     emailId=data.get('emailId')
     password=data.get('password')
     print emailId,password
     flag=False
     try:
          teacher=Teacher.objects.get(emailId=emailId)
          if teacher.emailId==emailId and teacher.password==password:
               flag=True
               request.session['teacher']=emailId
               return HttpResponseRedirect('/home')
          else:
               flag=False
     except Exception,e:
          error=e
    return render(request,'home/login.html',{"error":error})


def logout(request):
      del request.session['teacher']
      return HttpResponseRedirect('/home')


def help(request):
      teacher = onTeacher(request)
      return render(request,'home/help.html',{'user':teacher})



def history(request,year=0,month=0,day=0):

    teacher=onTeacher(request)
    attendanceList=Attendance.objects.filter(teacher=teacher)
    return render(request,'home/history.html',{'attendanceList':attendanceList,'user':teacher})


def getimageslables(course,branch,batch):
            students=Student.objects.filter(course__iexact=course,branch__iexact=branch,batch__iexact=batch) # __iexact ignore case
            images=[]
            lables=[]
            for student in students:
                for image in student.imagedata_set.all():
                    lables.append(int(student.rollNumber))
                    img='media/%s' % image
                    img=cv2.imread(img)
                    img=cv2.resize(img,(600,600),interpolation=cv2.INTER_AREA)
                    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    images.append(img)
            return images ,lables


#testing all type algo
def getpredictABC(r1,r2,r3,frame):
    face=obj.Face(1.6,5,20,20)
    faces=face.getFaces(frame)
    print "No of faces found",len(faces)
    abclist=[]
    for f in faces:
           simg=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
           simg=cv2.resize(simg,(600,600),interpolation=cv2.INTER_AREA)
           a=r1.getLable(simg)
           b=r2.getLable(simg)
           c=r3.getLable(simg)
           abclist.append(( a,b,c))
    return abclist

def getpredictLable(trainObj,frame):
    face=obj.Face(1.6,5,20,20)
    faces=face.getFaces(frame)
    print "No of faces found",len(faces)
    predictFace=[]
    for f in faces:
           simg=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
           simg=cv2.resize(simg,(600,600),interpolation=cv2.INTER_AREA)
           a=trainObj.getLable(simg)
           predictFace.append(a)
    return predictFace

#testing all type algo
def getr1r2r3(request):
      branch,course,batch=getBranchCourseBatch(request)
      images,lables=getimageslables(course,branch,batch)
      print images,lables
      r1 = rec.Recognizer()
      r2 = rec.Recognizer()
      r3 = rec.Recognizer()
      r1.train(images,lables,0)
      r2.train(images,lables,1)
      r3.train(images,lables,2)
      return r1,r2,r3



def unsetBranchCourseBatch(request):
        request.session['branch']=None
        request.session['course']=None
        request.session['batch']=None

def setBranchCourseBatch(request):
    try:
        branch=request.POST.get('branch')
        course=request.POST.get('course')
        batch=request.POST.get('batch')
        request.session['branch']=branch
        request.session['course']=course
        request.session['batch']=batch
        print "set=",course,branch,batch
        return True
    except:
        print "Somthing wrong with set branch , course , batch"
        return False


def getBranchCourseBatch(request):
    course=request.session.get('course')
    branch=request.session.get('branch')
    batch=request.session.get('batch')
    return branch,course,batch




#test all algo
r1=None  #LBPH train object
r2=None  #fisherfaces train object
r3=None  #eigenfaces  train object
def TESTstartcapturing(request):
      global r1,r2,r3
      print "come1"
      setBranchCourseBatch(request)
      print "come2"
      r1,r2,r3=getr1r2r3(request)
      print r1,r2,r3
      return HttpResponse("done")


#eigenfaces
def eigenfaces(request):
      branch,course,batch=getBranchCourseBatch(request)
      images,lables=getimageslables(course,branch,batch)
      ef=rec.Recognizer()
      print "Training Start ...",lables
      ef.train(images,lables,2)
      print "Training Done"
      return ef

#ef global train objects
ef=None
def startcapturing(request):
      global ef
      print "startcapturing function start"
      if setBranchCourseBatch(request):
          ipwebcamurl=request.POST.get('ipwebcamurl')
          if ipwebcamurl:
                print "web cam ip set",ipwebcamurl
                request.session['ipwebcamurl']=ipwebcamurl
          print "branch course batch set"
          ef=eigenfaces(request)
          if ef:
            print "Training eigenfaces object done"
            return HttpResponse("done")
          else:
              print "ef not created ef=",ef
              return HttpResponse(status=410)

      else:
          return HttpResponse("failed")


def handle_uploaded_file(f,name):
    imagePath='media/'+name
    imageSavePath='media/'+imagePath
    with open(imageSavePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return imagePath


def mupload(request):
    images=request.FILES.getlist('file')
    i=0
    for image in images:
          print i
          i+=1
          imagePath=handle_uploaded_file(image,image.name)
          rollNumber=image.name.split(".")[0]  # demo 12103074.9 -> 12103074
          imgd=ImageData()
          imgd.image=imagePath
          student=getStudent(rollNumber)
          if student :
              imgd.student = student
              imgd.save()
          else:
             print "error rollNumber:",rollNumber
    return HttpResponse("done")



def domore(request):
    if request.session.get('teacher',None):
        teacher=onTeacher(request)
        return render(request,'home/domore.html',{'user': teacher})
    else:

       return HttpResponseRedirect('/login')





def webcamcapture(request):
        if request.session.get('teacher',None):
            teacher=onTeacher(request)
            bcb = getBranchCourseBatch(request)
            if not all(bcb):
                 print "bcb not found:",getBranchCourseBatch(request)
                 return HttpResponseRedirect("/home/")
            return render(request,'home/webcamcapture.html',{'user':teacher,'bcb':bcb})
        else:
           return HttpResponseRedirect('/login')





#this function take Inmemoryuploadedfile and save into temp file read as openCV image and return then del tem
def get_uploaded_image(f,name):
    imagePath='media/'+name
    imageSavePath='media/'+imagePath
    with open(imageSavePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    img=cv2.imread(imageSavePath)
    os.remove(imageSavePath)
    return img

#this function get webcam.upload using FILES upload method
#csrf_exempt remove csrf missing server side error

# take image frop ip web cam and then predict the faces
@csrf_exempt
def ipcamimage(request):
    ipwebcamurl=request.session.get('ipwebcamurl')
    if ipwebcamurl:
        cap=cv2.VideoCapture(ipwebcamurl)
        ret,frame=cap.read()
        if ret:
            imagePridictor(frame)
            return HttpResponse("done")


# take image frop webcam and then predict the faces
@csrf_exempt
def webcamimage(request):
       global ef
       if not ef:
           ef=eigenfaces(request)
       teacher=onTeacher(request)
       import pickle
       type(r1)
       if request.FILES:
           image=request.FILES.get('webcam')
           image=get_uploaded_image(image,teacher.emailId)
           imagePridictor(image)
           return HttpResponse("done")


#take image obj as argument and predict the faces lable
def imagePridictor(image):
     output=getpredictLable(ef,image)
     if len(output)>0:
           txt="%s"%output
           l=Log()
           l.text=txt
           l.save()
     print output


def ipwebcamcapture(request):
      teacher=onTeacher(request)
      ipwebcamurl=request.session.get('ipwebcamurl')
      if ipwebcamurl and teacher:
           return render(request,'home/ipwebcamcapture.html',{'user':teacher,'ipwebcamurl':ipwebcamurl})
      else:
           return HttpResponseRedirect('/home')

#--------------------------------------------------------#
def HAdecisionAlgorithm(listPridictdata):
      print "I will come soon"


def profile(request):
    teacher=onTeacher(request)
    if teacher:
        return render(request,'home/profile.html',{'user':teacher})
    else:
        return HttpResponseRedirect('/home')

def done(request):
    pass
