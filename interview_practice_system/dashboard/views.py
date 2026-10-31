from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg

from interview.models import Answer, InterviewSession


class LandingView(TemplateView):
    template_name = "landing.html"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        solved_questions = Answer.objects.filter(
            interview__user=self.request.user
        ).count()

        sessions_completed = InterviewSession.objects.filter(
            user=self.request.user
        ).count()

        average = (
            Answer.objects.filter(
                interview__user=self.request.user,
                ai_score__isnull=False
            ).aggregate(avg=Avg("ai_score"))["avg"]
        )

        context["stats"] = {
            "solved_questions": solved_questions,
            "sessions_completed": sessions_completed,
            "avg_score": round(average, 1) if average else 0,
        }

        return context