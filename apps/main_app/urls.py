from django.conf.urls import url
import views

urlpatterns = [ 
    url(r'^$', views.index, name='home'),
    url(r'^create$', views.add, name='create'),
    url(r'^(?P<task_id>\d+)/show$', views.showUpdate, name='show_update'),
    url(r'^(?P<task_id>\d+)/udpate$', views.update, name='update'),
    url(r'^(?P<task_id>\d+)$', views.showDelete, name='show_delete'),
    url(r'^(?P<task_id>\d+)/delete$', views.delete, name='delete')
   
    
]