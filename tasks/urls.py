from django.urls import path
from .views import *

urlpatterns = [
    # path('', showtasks, name='showtasks'),
    path('', ShowTasks.as_view(), name='showtasks'),
    path('add/', AddTask.as_view(), name='addtask'),
    path('update/<int:tasks_id>/', UpdateTasks.as_view(), name='update_tasks'),
    path('delete/<int:tasks_id>/', DeleteTask.as_view(), name='delete'),
    path('task/<int:tasks_id>/', DetailTask.as_view(), name='task'),
    path('myprofile/<slug:slug>/', MyProfile.as_view(), name='profile'),
    path('profile/<slug:slug>/', ShowProfile.as_view(), name='show_profile'),
    path('add_friend/<slug:slug>/', AddFriend.as_view(), name='add_friend'),
    path('remove_friend/<slug:slug>/', RemoveFriend.as_view(), name='remove_friend'),
    # path('new_followers/<slug:slug>/', NewFollowers.as_view(), name='new_followers'),
    path('search/', search, name='search'),
    path('search_tasks/', search_task, name='search_task'),

]
