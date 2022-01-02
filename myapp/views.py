from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.http import HttpResponse
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.stem import SnowballStemmer
import subprocess
from django.http import FileResponse
import os
import time 
#import speech_recognition as sr
from nltk.stem.isri import ISRIStemmer
import cv2
def qr_to_path():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    result=None
    while True:
      _, img = cap.read()
      data, vertices_array, _ = detector.detectAndDecode(img)
      if vertices_array is not None:
        if data:
            result=data
            break    
      cv2.imshow("img", img)
      if cv2.waitKey(1) == ord("q"):
        break
    cap.release()
    cv2.destroyAllWindows()
    return result
class static:
    z={}
    result='No Thing'
    path=''
def audio_search():
    
    return 'laya'

def laya_matching(data,query):
    def steming(data):
        stemmer = SnowballStemmer('english')
        st = ISRIStemmer()
        #st.stem(w)
        result=''
        for x in data.lower().split(' '):
            result+=st.stem(x)+' '
        return result[:-1]
    matching=0
    matching_list=[]
    matching_path=[]
    matching_titles=[]
    for f in data:
        matching=0
        for word in steming(query).split(' '):
            if word in steming(f['title']) or word in steming(f['key_word']):
                matching+=1
        matching_list.append(matching)
        matching_path.append(f['path'])
        matching_titles.append(f['title'])
    return matching_list,matching_path,matching_titles
def matching_sort(matching_list,matching_path,matching_titles):
    sorted_matching_path=[]
    sorted_matching_titles=[]
    length=len(matching_list)
    for x in range(length):
        index=matching_list.index(max(matching_list))
        sorted_matching_path.append(matching_path[index])
        sorted_matching_titles.append(matching_titles[index])
        del matching_list[index]
        del matching_path[index]
        del matching_titles[index]
    return sorted_matching_titles,sorted_matching_path

# Create your views here.
def home(request):
    learning_type=''
    if request.POST.get('main',None):
             return redirect('home')
    if request.method=='POST':
         

        learning_type=request.POST.get('learning type')
        if learning_type=='1':
            return redirect('text_view')
        elif learning_type=='2':
            return redirect('video_view')
        else:
            return render(request,'home.html')
    return render(request,'home.html')
def text_view(request):
    if request.POST.get('main',None):
             return redirect('home')
    search='# *'
    d=None
    if request.method=='POST':
        print(request.POST)
        if request.POST.get('read_btn',None):
            context={
            'results':static.result,
            'title_path':static.z,
            'path':static.z[request.POST.get('result')]
               }
            return render(request,'textfile.html',context)
            
        if request.POST.get('search_btn',None):
            search=request.POST.get('search')
            files=FilesModel.objects.all()
            text_files=list(files.filter(file_type='text').values())
            print(search)
            a,b,c=laya_matching(text_files,search)
            d,e=matching_sort(a,b,c)
            static.result=d
            z=dict(zip(d,e))
            static.z=z
            context={
                'results':d,
                'title_path':z,
                'read':True
            }
            return render(request,'textfile.html',context)
    if request.POST.get('audio_btn',None):
        try:
            search=audio_search()
        except:
            search='error'
        files=FilesModel.objects.all()
        text_files=list(files.filter(file_type='text').values())
        print(search)
        a,b,c=laya_matching(text_files,search)
        d,e=matching_sort(a,b,c)
        static.result=d
        z=dict(zip(d,e))
        static.z=z
        context={
                'results':d,
                'title_path':z,
                'read':True
            }
        return render(request,'textfile.html',context)
    if request.POST.get('QR_btn',None):
        search= qr_to_path()
        files=FilesModel.objects.get(path=search)
        print(files.title)
        #a,b,c=laya_matching(text_files,search)
        #d,e=matching_sort(a,b,c)
        static.result=[files.title]
        #z=dict(zip(d,e))
        #static.z=z
        context={
                'path':search,
                'results':static.result,
                 'read':None
            }
        return render(request,'textfile.html',context)
    context={
            'results':d,
            'title_path':None
        }
        
    return render(request,'textfile.html',context)

def video_view(request):
    if request.POST.get('main',None):
             return redirect('home')
    search='# *'
    d=None
    if request.method=='POST':
        print(request.POST)
        if request.POST.get('read_btn',None):
            context={
            'results':static.result,
            'title_path':static.z,
            'path':static.z[request.POST.get('result')]
               }
            return render(request,'videofile.html',context)
            
        if request.POST.get('search_btn',None):
            search=request.POST.get('search')
            files=FilesModel.objects.all()
            video_files=list(files.filter(file_type='video').values())
            print(search)
            a,b,c=laya_matching(video_files,search)
            d,e=matching_sort(a,b,c)
            static.result=d
            z=dict(zip(d,e))
            static.z=z
            context={
                'results':d,
                'title_path':z,
                'read':True
            }
            return render(request,'videofile.html',context)
    if request.POST.get('audio_btn',None):
        try:
            search=audio_search()
        except:
            search='error'
        files=FilesModel.objects.all()
        video_files=list(files.filter(file_type='video').values())
        print(search)
        a,b,c=laya_matching(video_files,search)
        d,e=matching_sort(a,b,c)
        static.result=d
        z=dict(zip(d,e))
        static.z=z
        context={
                'results':d,
                'title_path':z,
                'read':True
            }
        return render(request,'videofile.html',context)
    if request.POST.get('QR_btn',None):
        search= qr_to_path()
        print(search)
        files=FilesModel.objects.get(path=search)
        print(files.title)
        #a,b,c=laya_matching(text_files,search)
        #d,e=matching_sort(a,b,c)
        static.result=[files.title]
        #z=dict(zip(d,e))
        #static.z=z
        context={
                'path':search,
                'results':static.result,
                'read':None
                 
            }
        return render(request,'videofile.html',context)
    context={
            'results':d,
            'title_path':None
        }
        
    return render(request,'videofile.html',context)
