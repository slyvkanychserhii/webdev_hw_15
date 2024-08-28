from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    # http://127.0.0.1:8000/api/tasks
    path(
        'tasks/',
        TaskListCreateView.as_view(),
        name='task-list-create'),
    # http://127.0.0.1:8000/api/tasks/1
    path(
        'tasks/<int:pk>',
        TaskRetrieveUpdateDestroyView.as_view(),
        name='task-retrieve-update-destroy'),
    # http://127.0.0.1:8000/api/tasks/statistics
    path(
        'tasks/statistics/',
        TaskStatisticsView.as_view(),
        name='task-statistics'),
    # http://127.0.0.1:8000/api/subtasks
    path(
        'subtasks/',
        SubTaskListCreateView.as_view(),
        name='subtask-list-create'),
    # http://127.0.0.1:8000/api/subtasks/1
    path(
        'subtasks/<int:pk>',
        SubTaskRetrieveUpdateDestroyView.as_view(),
        name='subtask-retrieve-update-destroy'),
    # http://127.0.0.1:8000/api/categories
    # http://127.0.0.1:8000/api/categories/1
    # http://127.0.0.1:8000/api/categories/count_tasks
    path('', include(router.urls)),
]
