from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Max

from interview.models import Answer


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "performance/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        answers = Answer.objects.filter(interview__user=self.request.user)

        total_attempts = answers.count()

        average_score = answers.aggregate(
            Avg("ai_score")
        )["ai_score__avg"] or 0

        highest_score = answers.aggregate(
            Max("ai_score")
        )["ai_score__max"] or 0

        recent_answers = answers.order_by("-created_at")[:10]

        context["total_attempts"] = total_attempts
        context["average_score"] = round(average_score, 2)
        context["highest_score"] = highest_score
        context["recent_answers"] = recent_answers

        return context