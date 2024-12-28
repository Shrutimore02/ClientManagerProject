# clients/views.py

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, ClientCreateSerializer, ProjectDetailSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.models import User




# List all clients and create a new client
class ClientListCreateAPIView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Retrieve, update or delete a client
class ClientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        """
        Override to automatically assign the 'created_by' field to the logged-in user.
        """
        serializer.save(created_by=self.request.user)

# List all projects assigned to the logged-in user
class ProjectListForUserAPIView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Create a new project for a specific client and assign users to it
class ProjectCreateAPIView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client_id = self.kwargs.get('client_id')
        client = Client.objects.get(id=client_id)
        users = serializer.validated_data.get('users')

        project = serializer.save(client=client, created_by=self.request.user)
        project.users.set(users)  # Assign users to the project


# Endpoint to create a project for a client
@api_view(['POST'])
def create_project_for_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    # Extract project details from the request
    project_name = request.data.get('project_name')
    user_ids = [user['id'] for user in request.data.get('users', [])]
    users = User.objects.filter(id__in=user_ids)

    if not project_name or not users.exists():
        return Response({"error": "Project name or users are invalid"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the project
    project = Project.objects.create(
        project_name=project_name,
        created_by=request.user,
        client=client
    )
    project.users.set(users)

    # Serialize the response
    serializer = ProjectDetailSerializer(project, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)



class ClientDetailAPIView(RetrieveAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Use the specific serializer for this endpoint
        return ClientDetailSerializer
