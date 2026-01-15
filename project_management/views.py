from django.shortcuts import render
from .serializers import CompanySerializer, ProjectSerializer, TaskSerializer
from .models import Company, Project, Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .permissions import IsStaffOrReadOnly, IsAdmin, IsManagerOrIsAdmin, IsUserOrAbove


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# class ProjectViewSet(ModelViewSet):
#     queryset = Project.objects.all().order_by('-created_at')
#     serializer_class = ProjectSerializer
#
#     def get_permissions(self):
#         if self.action in ["create", "list", "update", "partial_update", "destroy", "retrieve"]:
#             return [IsAuthenticated(), IsManagerOrIsAdmin()]
#         return [IsAuthenticated()]


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()  # REQUIRED for router
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Project.objects.none()

        # Admin / Manager → full access
        if user.profile.role in ["admin", "manager"]:
            return Project.objects.all().order_by("-created_at")

        # # Normal users → no projects
        # return Project.objects.none()


        # Normal user → only projects where user has tasks
        return (
            Project.objects
            .filter(tasks__assigned_to=user)
            .distinct()
            .order_by("-created_at")
        )

    def get_permissions(self):
        if self.action in [
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [IsAuthenticated(), IsManagerOrIsAdmin()]
        return [IsAuthenticated()]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related("project", "assigned_to").order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsUserOrAbove()]

