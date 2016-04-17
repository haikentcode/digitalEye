from django.contrib import admin
from home.models import *


class Attendance_Admin(admin.ModelAdmin):
    list_display=['teacher','date']
    filter_horizontal = ('students',)


class Teacher_Admin(admin.ModelAdmin):
    list_display=['emailId','contactNo','image_tag']

class Student_Admin(admin.ModelAdmin):
    list_display=['rollNumber','branch','batch','course','date','get_images']
    def get_images(self,obj):
          images=""
          for image in obj.imagedata_set.all():
              images+=u'<img src="/media/%s" width="100px" height="100px"/>' % image
          return images
    get_images.short_description = 'Item Image'
    get_images.allow_tags = True



class ImageData_Admin(admin.ModelAdmin):
      list_display = ['student','image_tag']

admin.site.register(Student,Student_Admin)
admin.site.register(ImageData,ImageData_Admin)
admin.site.register(Teacher,Teacher_Admin)
admin.site.register(Attendance,Attendance_Admin)
