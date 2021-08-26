from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('jobs/new', views.new),
    path('jobs/new/create', views.create),
    path('addjob/<int:job_id>', views.addjob),
    path('removejob/<int:job_id>', views.removejob),
    path('jobs/<int:job_id>', views.viewjob),
    path('jobs/<int:job_id>/edit', views.edit),
    path('jobs/<int:job_id>/update', views.update),
    path('jobs/<int:job_id>/delete', views.delete),
]