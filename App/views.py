import mimetypes
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Group, Sub_group, index_file

def index(request):

    data = index_file.objects.all()

    context = {
        "datas":data,
        }
    return render(request, 'index.html', context=context)

def files(request):

    data = Group.objects.all()
    context = {
        "datas": data  
            }
    return render(request, 'files.html', context)


def sub_files(request, id):

    group = get_object_or_404(Group, id= id)
    sub_group = Sub_group.objects.filter(group=group)
    return render(request, 'sub_file.html', {"groups":group, "sub_groups": sub_group})


def download_file(request, id):
    sub_group = get_object_or_404(Sub_group, id=id)

    if not sub_group.file:
        raise Http404("No file uploaded")

    file_name = sub_group.file.name
    storage = sub_group.file.storage

    if not storage.exists(file_name):
        raise Http404("File not found")

    file_obj = storage.open(file_name, 'rb')
    content_type, _ = mimetypes.guess_type(file_name)
    response = FileResponse(file_obj, content_type=content_type or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_name)}"'
    return response


@login_required
def dashboard(request):

    files = Sub_group.objects.filter(user = request.user)

    if request.user.is_superuser or request.user.is_staff:
        role = "admin"
    else:
        role = "user"

    return render(request, 'dashboard.html', {
        "username": request.user.username,
        "email" : request.user.email, 
        "role": role,
        "name": request.user.first_name,

        "files" : files

    })

from django.conf import settings


def check_media(request):
    """Check where files are actually saving"""
    media_root = str(settings.MEDIA_ROOT)
    files_dir = os.path.join(media_root, 'files')
    
    # List files in the directory
    files_list = []
    if os.path.exists(files_dir):
        files_list = os.listdir(files_dir)
    
    data = {
        'media_root': media_root,
        'media_exists': os.path.exists(media_root),
        'files_dir': files_dir,
        'files_exists': os.path.exists(files_dir),
        'files_in_directory': files_list,
    }
    
    return JsonResponse(data)

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
  
        try: 
            if User.objects.filter(email = username).exists():
                user = User.objects.get(email=username)
                username = user.username

        except User.DoesNotExist:
            pass
            

        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect('dashboard')
        
        else:
            return render(request, 'login.html', {"error": 'Invalid credential'})



    return render(request, 'login.html')

@login_required
def file_upload(request, id):
    if request.method == "POST":
        heading = request.POST.get("heading")
        description = request.POST.get("descri")
        files_ = request.FILES.get('file')
        
        group = get_object_or_404(Group, id=id)
        
        if description == "":
            description = "None" 
        
        if not files_:
            return render(request, "file_upload.html", {'error': 'Please select a file'})
        
        # DEBUG: Print where file will be saved
        print(f"📁 File name: {files_.name}")
        print(f"📁 File size: {files_.size}")
        print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        datas = Sub_group(
            user=request.user, 
            heading=heading, 
            description=description, 
            file=files_, 
            group=group
        )
        datas.save()
        
        # DEBUG: Check if file was actually saved
        if datas.file:
            print(f"✅ File saved at: {datas.file.path}")
            print(f"✅ File exists: {os.path.exists(datas.file.path)}")
        else:
            print("❌ File was NOT saved!")
        
        return redirect('files')
    
    return render(request, "file_upload.html")

def signup(request):

    if request.method == "POST" :
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confrim_password = request.POST.get("confro_pass")

        if User.objects.filter(username = username).exists():

            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })

        if User.objects.filter(email = email).exists():

            return render(request, 'signup.html', {
                'error': 'Email already exists'
            })
        

        if password != confrim_password:
            return render(request, 'signup.html', {'error': "Password and Confrim Password did not match"})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        return redirect('login')




    return render(request, "signup.html")


def logout_view(request):

    logout(request)
    return redirect('login')



@login_required
def create_group(request):


    if request.method == "POST":

        heading = request.POST.get("heading")
        description = request.POST.get("descri")
        print(heading, description)
        group = Group(user=request.user, heading=heading, description=description)

        group.save()
        return redirect('files')

    return render(request, 'group_upload.html')



