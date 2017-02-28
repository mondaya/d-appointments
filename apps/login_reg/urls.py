from django.conf.urls import url,include
import views

urlpatterns = [ 
    url(r'^$', views.index, name='signup'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$',views.registration, name='register'),
    url(r'^logout$', views.logout, name='logout' ),
    url(r'^success$', views.success, name='success' ),
]