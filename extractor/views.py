from django.shortcuts import render
from .Presentor import info_Extractor
import os
from docinfo.settings import BASE_DIR
from django.core.files.storage import FileSystemStorage
media = 'media'
from django import forms
from django.db import models

class MyImage(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)


def index(request):
    if request.method == "POST" and request.FILES['upload']:
        if 'upload' not in request.FILES:
            err = 'No image Selected'
            return render(request,'index.html',{'err':err})
        f = request.FILES['upload']
        if f== '':
            err = 'No file Selected'
            return render(request,'index.html',{'err':err})
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name,upload)
        file_url = fss.url(file)
        card_type = request.POST['card_type']
        img_path = os.path.join(BASE_DIR,media,file)

        predictions = info_Extractor(card_type,img_path)
        return render(request,"index.html",{'pred':predictions,'file_url':file_url,'img':img_path})

    else:
        return render(request,"index.html") 
    
