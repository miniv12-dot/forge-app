from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import DailyLog, TopicCategory, CommunityPost, Comment
from .serializers import DailyLogSerializer, TopicCategorySerializer, CommunityPostSerializer, CommentSerializer
from django.utils import timezone

# --- TRACKING VIEWS ---
class DailyLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer
    permission_classes = [AllowAny] 


    def get_queryset(self):
        # Fallback query pattern for authenticated users in production
        if self.request.user.is_authenticated:
            return DailyLog.objects.filter(user=self.request.user).order_by('-date')
        return DailyLog.objects.none()

    def list(self, request, *args, **kwargs):
        """DEMO MODE: Intercept list requests and read logs from browser cookie memory."""
        if not request.user.is_authenticated:
            demo_logs = request.session.get('demo_logs', [])
            return Response(demo_logs)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """DEMO MODE: Intercept post requests and append metrics to current session array."""
       # IF USER IS ANONYMOUS (Demo / Guest Runner)
        if not request.user.is_authenticated:
            data = request.data 
            
            if 'demo_logs' not in request.session:
                request.session['demo_logs'] = []
            
            # Grab the specific date the frontend sent us (Fallback to today if it fails)
            provided_date = data.get('date', timezone.now().date().isoformat())
            
            mock_log = {
                "id": len(request.session['demo_logs']) + 1,
                "date": provided_date, # Saves the specific clicked day
                "sleep_hours": data.get('sleep_hours', 0), # Added sleep_hours
                "training_done": data.get('training_done', False),
                "mental_state": data.get('mental_state', {"stress": 0, "energy": 0, "clarity": 0}) # Added clarity
            }
            
            request.session['demo_logs'].insert(0, mock_log)
            request.session.modified = True
            
            return Response(mock_log, status=status.HTTP_201_CREATED)
            
                        
            # Prepend to array to ensure 'Just Now' items always render on top
            request.session['demo_logs'].insert(0, mock_log)
            request.session.modified = True
            
            return Response(mock_log, status=status.HTTP_201_CREATED)
            
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def insights(self, request):
        """DEMO MODE: Manually parse data array averages if user is a guest."""
        if not request.user.is_authenticated:
            demo_logs = request.session.get('demo_logs', [])
            
            t_stress, t_energy, t_count = 0, 0, 0
            r_stress, r_energy, r_count = 0, 0, 0
            
            for log in demo_logs:
                m_state = log.get('mental_state', {})
                # Ensure structure is read accurately if nested dictionary patterns exist
                stress = m_state.get('stress', 0) if isinstance(m_state, dict) else 0
                energy = m_state.get('energy', 0) if isinstance(m_state, dict) else 0
                
                if log.get('training_done'):
                    t_stress += stress
                    t_energy += energy
                    t_count += 1
                else:
                    r_stress += stress
                    r_energy += energy
                    r_count += 1

            return Response({
                "analysis_type": "Habit Correlation (Demo Mode)",
                "training_days": {
                    "average_stress": round(t_stress / t_count, 2) if t_count > 0 else 0,
                    "average_energy": round(t_energy / t_count, 2) if t_count > 0 else 0
                },
                "rest_days": {
                    "average_stress": round(r_stress / r_count, 2) if r_count > 0 else 0,
                    "average_energy": round(r_energy / r_count, 2) if r_count > 0 else 0
                }
            })

        # PRODUCTION MODE: Read statistical models from PostgreSQL tables
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
    permission_classes = [AllowAny] 

class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all().order_by('-created_at')
    serializer_class = CommunityPostSerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        demo_user = User.objects.first()
        serializer.save(author=demo_user)