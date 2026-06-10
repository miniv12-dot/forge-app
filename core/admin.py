from django.contrib import admin
from .models import (
    UserProfile, DailyLog, MentalState, 
    TopicCategory, CommunityPost, Comment
)

# --- TRACKING MODELS ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'streak_count', 'created_at')
    search_fields = ('user__username',)

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'sleep_hours', 'training_done')
    list_filter = ('training_done', 'date')

@admin.register(MentalState)
class MentalStateAdmin(admin.ModelAdmin):
    list_display = ('log', 'energy', 'stress', 'clarity')
    list_filter = ('energy', 'stress')


# --- COMMUNITY MODELS ---
@admin.register(TopicCategory)
class TopicCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')