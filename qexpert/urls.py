from django.conf.urls import url,include
from django.contrib import admin
from mainsite import views as main_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_views.home, name='home'),
    url(r'^login/$', main_views.login, name='login'),
    url(r'^signup/$', main_views.signup, name='signup'),
    url(r'^logout/$', main_views.logout, name='logout'),
]
