# clients/serializers.py

from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User



# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']


# Serializer for the Project model
class ProjectSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by']

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Customize the project output to match expected output
        representation['created_by'] = instance.created_by.username
        representation['created_at'] = instance.created_at
        return representation





# Serializer for the Client model
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username',  read_only=True)
    projects = ProjectSerializer( many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at','updated_at', 'created_by','projects']
        read_only_fields = ['created_at', 'created_by', 'updated_at']  # Ensure created_at, created_by, and updated_at are read-only


    def to_representation(self, instance):
        """
        Customize the default representation to handle different request methods.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # If the request method is PUT or PATCH, remove the 'projects' field
        if request and request.method in ['PUT', 'PATCH']:
            representation.pop('projects', None)
        
        # For GET requests, we show projects with only the id and project_name fields
        if request and request.method == 'GET':
            # Ensure 'created_at' and 'created_by' are not part of the project representation
            for project in representation['projects']:
                project.pop('created_at', None)
                project.pop('created_by', None)

        return representation



class ClientCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at','created_by']
        read_only_fields = ['created_at','created_by']  # 'created_at' and 'created_by' will be set automatically


class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'updated_at', 'created_by', 'projects']

    def get_projects(self, instance):
        # Return only 'id' and 'project_name' for projects
        return [{'id': project.id, 'project_name': project.project_name} for project in instance.projects.all()]


class ProjectDetailSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.client_name', read_only=True)
    users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

    def get_users(self, obj):
        return [{'id': user.id, 'name': user.username} for user in obj.users.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = instance.created_by.username
        return representation
