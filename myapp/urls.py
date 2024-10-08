from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    SigninView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)


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
    # http://127.0.0.1:8000/api/token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # http://127.0.0.1:8000/api/token/refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # http://127.0.0.1:8000/api/signin
    path('signin/', SigninView.as_view(), name='signin'),
    # path('signup/', SignupView.as_view(), name='signup'),
    # path('signout/', SignoutView.as_view(), name='signout'),
]
