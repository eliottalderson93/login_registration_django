from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index), #template for registration
    url(r'^users$', views.index), #template
    url(r'^users/logout$', views.logout), #post #updates the DB and redirects to users
    url(r'^users/add$', views.create), #post create user
    url(r'^users/login$', views.login), #login validation
    url(r'^users/(?P<id>\d+)$', views.show), #template for success
    url(r'^users/login_page$', views.login_page), #template for login
    #url(r'^users/(?P<id>\d+)/delete$', views.destroy) #post
]
