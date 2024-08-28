from django.utils import timezone
from rest_framework.serializers import (
    ValidationError,
    ModelSerializer,
    DateTimeField)
from .models import (
    Category,
    Task,
    SubTask)


def validate_deadline(value):
    if value < timezone.now():
        raise ValidationError(
            "The deadline cannot be in the past")
    return value


class CategorySerializer(ModelSerializer):
    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise ValidationError(
                'A category with this name already exists')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        pk = instance.pk
        if Category.objects.filter(name=name).exclude(pk=pk).exists():
            raise ValidationError(
                'A category with this name already exists')
        return super().update(instance, validated_data)

    class Meta:
        model = Category
        fields = '__all__'


class SubTaskSerializer(ModelSerializer):
    deadline = DateTimeField(
        required=False,
        validators=[validate_deadline])

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class TaskSerializer(ModelSerializer):
    deadline = DateTimeField(
        required=False,
        validators=[validate_deadline])
    sub_tasks = SubTaskSerializer(
        read_only=True,
        many=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at']
