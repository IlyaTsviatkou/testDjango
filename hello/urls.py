from django.contrib import admin
from django.conf.urls import include,url
from django.urls import path
from firstapp import views
from django.contrib.auth import views as vw

urlpatterns = [
    path('', views.index),
    path('index', views.index,name="index"),
    path('player', views.player_out),
    path('org', views.org, name="org"),
    path('kab', views.kabinet, name="kabinet"),
    path('about', views.about),
    path('create/', views.create),
    #path('edit/<int:id>/', views.edit),
    #path('delete/<int:id>/', views.delete),
    path('take_org/<int:id>/', views.take_org),
    path('put_org/', views.put_org),
    path('take_course/<int:id>/', views.take_course),
    path('put_course/<int:id>/', views.put_course),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #('^hello/$', hello),
    #url(r'^login/$', views.user_login, name='login'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    path('login', views.MyprojectLoginView.as_view(), name='login_page'),
    path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('logout', views.MyProjectLogout.as_view(), name='logout_page'),
    url(r'^confirmation/(?P<name>[-\w]+)/', views.page_confirmation, name="confirmation"),
    
]
