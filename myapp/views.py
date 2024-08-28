from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import (
    Category,
    SubTask,
    Task,
    StatusType)
from .serializers import (
    CategorySerializer,
    SubTaskSerializer,
    TaskSerializer)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'previous_link': self.get_previous_link(),
            'next_link': self.get_next_link(),
            'results': data
        })


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # http://127.0.0.1:8000/api/categories/count_tasks/
    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        tasks_by_category = Category.objects.annotate(
            task_count=Count('tasks'))
        data = [
            {
                "category_id": category.id,
                "category_name": category.name,
                "task_count": category.task_count
            }
            for category in tasks_by_category
        ]
        return Response(data)


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Фильтрация по полям status и deadline_lt:
    # http://127.0.0.1:8000/api/subtasks/?status=1
    # http://127.0.0.1:8000/api/subtasks/?deadline__lt=2024-09-27T00:00:00Z
    # http://127.0.0.1:8000/api/subtasks/?deadline__gt=2024-09-27T00:00:00Z
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['exact', 'gt', 'lt'],
    }
    # Поиск по полям title и description:
    # http://127.0.0.1:8000/api/subtasks/?search=subtask_name
    search_fields = ['title', 'description']
    # Сортировка по полю created_at:
    # http://127.0.0.1:8000/api/subtasks/?ordering=created_at
    # Сортировка по полю created_at (по убыванию):
    # http://127.0.0.1:8000/api/subtasks/?ordering=-created_at
    ordering_fields = ['created_at']


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Фильтрация по полям status и deadline_lt:
    # http://127.0.0.1:8000/api/tasks/?status=1
    # http://127.0.0.1:8000/api/tasks/?deadline__lt=2024-09-27T00:00:00Z
    # http://127.0.0.1:8000/api/tasks/?deadline__gt=2024-09-27T00:00:00Z
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['exact', 'gt', 'lt'],
    }
    # Поиск по полям title и description:
    # http://127.0.0.1:8000/api/tasks/?search=task_name
    search_fields = ['title', 'description']
    # Сортировка по полю created_at:
    # http://127.0.0.1:8000/api/tasks/?ordering=created_at
    # Сортировка по полю created_at (по убыванию):
    # http://127.0.0.1:8000/api/tasks/?ordering=-created_at
    ordering_fields = ['created_at']


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskStatisticsView(APIView):
    def get(self, request):
        data = {}
        data['tasks'] = Task.objects.count()
        tasks_by_status = Task.objects.values(
            'status').annotate(task_count=Count('*'))
        data['tasks_by_status'] = [
            {
                "status": StatusType(status['status']).label,
                "tasks_count": status['task_count']
            }
            for status in tasks_by_status
        ]
        data['tasks_lt_now'] = Task.objects.filter(
            deadline__lt=timezone.now()).count()
        return Response(data, status=status.HTTP_200_OK)
