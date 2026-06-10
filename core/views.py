from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # Changed from IsAuthenticated
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import DailyLog, TopicCategory, CommunityPost, Comment
from .serializers import DailyLogSerializer, TopicCategorySerializer, CommunityPostSerializer, CommentSerializer

# --- TRACKING VIEWS ---
class DailyLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer
    permission_classes = [AllowAny] # Open for demo

    def get_queryset(self):
        # Demo: Just return all logs in the database
        return DailyLog.objects.all().order_by('-date')

    @action(detail=False, methods=['get'])
    def insights(self, request):
        # Demo: Calculate insights globally instead of per-user
        trained_logs = DailyLog.objects.filter(training_done=True)
        rest_logs = DailyLog.objects.filter(training_done=False)

        trained_stress = trained_logs.aggregate(Avg('mental_state__stress'))['mental_state__stress__avg'] or 0
        rest_stress = rest_logs.aggregate(Avg('mental_state__stress'))['mental_state__stress__avg'] or 0

        trained_energy = trained_logs.aggregate(Avg('mental_state__energy'))['mental_state__energy__avg'] or 0
        rest_energy = rest_logs.aggregate(Avg('mental_state__energy'))['mental_state__energy__avg'] or 0

        return Response({
            "analysis_type": "Habit Correlation",
            "training_days": {
                "average_stress": round(trained_stress, 2),
                "average_energy": round(trained_energy, 2)
            },
            "rest_days": {
                "average_stress": round(rest_stress, 2),
                "average_energy": round(rest_energy, 2)
            }
        })

# --- COMMUNITY VIEWS ---
class TopicCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TopicCategory.objects.all()
    serializer_class = TopicCategorySerializer
    permission_classes = [AllowAny] # Open for demo

class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all().order_by('-created_at')
    serializer_class = CommunityPostSerializer
    permission_classes = [AllowAny] # Open for demo

    def perform_create(self, serializer):
        # Demo: Automatically assign new posts to the first user in the database
        demo_user = User.objects.first()
        serializer.save(author=demo_user)