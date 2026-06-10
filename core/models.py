from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Links directly to Django's built-in User system
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    streak_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(auto_now_add=True)
    sleep_hours = models.FloatField()
    training_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Log for {self.user.username} on {self.date}"


class MentalState(models.Model):
    # 1:1 relationship with DailyLog; if a log is deleted, this is deleted too
    log = models.OneToOneField(DailyLog, on_delete=models.CASCADE, related_name='mental_state')
    
    # Mood metrics scaled from 1 to 10
    energy = models.IntegerField()
    stress = models.IntegerField()
    clarity = models.IntegerField()

    def __str__(self):
        return f"Mental Metrics for Log ID: {self.log.id}"
    

class TopicCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    # We will use this later on the frontend to show cool icons (like a fire emoji for Burnout)
    icon = models.CharField(max_length=50, blank=True, null=True) 

    def __str__(self):
        return self.name


class CommunityPost(models.Model):
    # Notice we still link to the real user in the database. 
    # The "Anonymity Engine" will hide this later in the API layer.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    category = models.ForeignKey(TopicCategory, on_delete=models.CASCADE, related_name='posts')
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by User ID {self.author.id} on Post {self.post.id}"