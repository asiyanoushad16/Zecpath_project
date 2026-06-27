from rest_framework import serializers
from .models import (
    User,
    Job,
    Candidate,
    Employer
)

import os


class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ['resume']

    def validate_resume(self, value):

        allowed_extensions = [
            '.pdf',
            '.doc',
            '.docx'
        ]

        extension = os.path.splitext(
            value.name
        )[1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOC and DOCX files are allowed."
            )

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size must be less than 5 MB."
            )

        return value
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'password',
            'role'
        ]

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def create(self, validated_data):

        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class JobSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="employer.company_name",
        read_only=True
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "skills",
            "experience",
            "salary",
            "location",
            "job_type",
            "company_name",
            "employer"
        ]

        extra_kwargs = {
            "employer": {
                "read_only": True
            }
        }


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }

    def validate_expected_salary(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Salary must be greater than zero."
            )

        return value

    def validate_experience(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Experience cannot be negative."
            )

        return value


class EmployerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employer
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }

    def validate_company_size(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Company size must be greater than zero."
            )

        return value
class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = [
                'id',
                'username',
                'email',
                'role'
            ]
    
