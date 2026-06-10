from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DailyLog, MentalState, TopicCategory, CommunityPost, Comment

# --- TRACKING SERIALIZERS ---

class MentalStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalState
        fields = ['energy', 'stress', 'clarity']

class DailyLogSerializer(serializers.ModelSerializer):
    mental_state = MentalStateSerializer() 

    class Meta:
        model = DailyLog
        fields = ['id', 'date', 'sleep_hours', 'training_done', 'mental_state']
        read_only_fields = ['id', 'date']

    def create(self, validated_data):
        mental_state_data = validated_data.pop('mental_state')
        
        # 1. Grab the first real user in the database
        demo_user = User.objects.first()
        
        # 2. Failsafe: If no users exist at all, create one instantly
        if not demo_user:
            demo_user = User.objects.create_user(username='demo_user', password='password')

        # 3. Save the log using ONLY the demo_user
        log = DailyLog.objects.create(user=demo_user, **validated_data)
        MentalState.objects.create(log=log, **mental_state_data)
        
        return log


# --- COMMUNITY SERIALIZERS ---

class TopicCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicCategory
        fields = ['id', 'name', 'description', 'icon']

class CommentSerializer(serializers.ModelSerializer):
    author_alias = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author_alias', 'content', 'created_at']

    def get_author_alias(self, obj):
        return f"User_{(obj.author.id * 837) % 9999}"

class CommunityPostSerializer(serializers.ModelSerializer):
    author_alias = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.name')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CommunityPost
        fields = ['id', 'author_alias', 'category', 'category_name', 'title', 'content', 'created_at', 'comments']
        read_only_fields = ['id', 'created_at']

    def get_author_alias(self, obj):
        return f"User_{(obj.author.id * 837) % 9999}"