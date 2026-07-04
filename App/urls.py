from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('files/', views.files, name='files'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('upload_file/<int:id>', views.file_upload, name='file_upload'),
    path('logout/', views.logout_view, name='logout'),
    path('sub_files/<int:id>', views.sub_files, name='sub_files'),
    path('create_group/', views.create_group, name="create_group")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)