from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^jobs/edit/(?P<id>\d+)$', views.edit_page),
    url(r'^jobs/update$', views.update),
    url(r'^jobs/new$', views.new_page),
    url(r'^add$', views.add_job),
    url(r'^jobs/(?P<id>\d+)$', views.job_page),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^add/(?P<id>\d+)$', views.work_job),
    url(r'^quit/(?P<id>\d+)$', views.quit_job)
]