from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^vitae/$', views.vitae, name='vitae'),
    url(r'^(?P<job_id>[0-9]+)/details/$', views.details, name='details'),
    url(r'^add/$', views.add, name='add'),
]