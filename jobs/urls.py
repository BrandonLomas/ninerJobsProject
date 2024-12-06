from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:pk>', views.job_detail, name='job_detail'),
    path('job/<int:pk>/apply', views.apply_for_job, name='apply_for_job'),
    path('add_job/', views.add_job, name='add_job'),
    path('edit_job/<int:pk>', views.edit_job, name='edit_job'),
    path('delete_job/<int:pk>', views.delete_job, name='delete_job'),
    path('job/<int:pk>/applications', views.view_applications, name='view_applications'),
    

]