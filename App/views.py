from django.shortcuts import render, redirect, get_object_or_404
from .models import index_file, Group, Sub_group
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

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
        
        # Add error handling for file upload
        if not files_:
            return render(request, "file_upload.html", {
                'error': 'Please select a file to upload'
            })
        
        try:
            datas = Sub_group(
                user=request.user, 
                heading=heading, 
                description=description, 
                file=files_, 
                group=group
            )
            datas.save()
            return redirect('files')
        except Exception as e:
            # This will help debug the issue
            print(f"Upload error: {e}")
            return render(request, "file_upload.html", {
                'error': f'Upload failed: {str(e)}'
            })
    
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



