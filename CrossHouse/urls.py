"""CrossHouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from CrossApp.views import AdDelete_View, AdUpdate_View, BlogDetailView, BlogView, BloggerProfilView, LogoutView, MyBlogView, Website_Manager, Login, Signup, All_User, Update_User,Admin_Register_User,\
    email_validate_view,activate,CreateAdForm_View,ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', Website_Manager.as_view(template_name='index.html'), name='home'),
    path('login/', Login.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('view_profil/<int:pk>/user', BloggerProfilView.as_view(template_name="profil_view.html"), name='view_profil'),
    path('update-user/', Update_User.as_view(), name='update-user'),
    path('register/', Signup.as_view(), name='register'),
    path('all_user/', All_User.as_view(template_name='users.html'), name='users'),
    path('admin_create_user/', Admin_Register_User.as_view(), name='admin_create_user'),
    path('settings/', Website_Manager.as_view(template_name='settings.html'), name='settings'),
    path('email-verification/', email_validate_view.as_view(), name='email-validate'),
    path('activate/<uidb64>/<token>',activate, name='activate'),
    path('create_ad/',CreateAdForm_View.as_view(), name='create_ad'),
    path('ad/<int:pk>/edit/',AdUpdate_View.as_view(), name='ad-edit'),
    path('ad/<int:pk>/delete/',AdDelete_View.as_view(), name='delete_ad'),
    path('blog/',BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/detail/',BlogDetailView.as_view(), name='blog_detail'),
    path('contact/',ContactView.as_view(), name='contact'),
    path('myblog/',MyBlogView.as_view(), name='myblog'),
    path('contact_seller/',Website_Manager.as_view(template_name='contact_seller.html'), name='contact_seller'),
    # path('blog/blog_rdv/',valide_rdv, name='blog_rdv'),
    ]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    


