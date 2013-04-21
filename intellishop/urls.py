from django.conf.urls import *

urlpatterns = patterns('',
                       url(r'^$', 'intellishop.views.home',name="home"),
                       url(r'^shops$', 'intellishop.views.shops',name="shops"),
                       url(r'^about$', 'intellishop.views.about', name='about'),
)

