from rest_framework import serializers
from . import models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['id', 'username', 'admin']  # Bạn có thể thêm hoặc bỏ bớt các trường theo nhu cầu

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminUser
        fields = ['id', 'email', 'name']
        
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['id', 'title', 'content', 'publish_date', 'admin_id']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'name', 'dob', 'score', 'preferences', 'account_id']
        
class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expert
        fields = ['id', 'name', 'email', 'field_of_expertise']
        
class ConsultationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Consultation
        fields = ['id', 'date', 'notes', 'expert_id', 'user_id']
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test 
        fields = ['id', 'test_name', 'test_type', 'description']
        
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ['id', 'score', 'timestamp', 'test_id', 'user_id']
        
class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Forum
        fields = ['id', 'topic', 'user_id']
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)