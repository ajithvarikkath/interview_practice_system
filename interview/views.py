from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

from .models import Question, InterviewSession, Answer
from .forms import AnswerForm
from .ai import evaluate_answer


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "interview/question_list.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.select_related("category").all()


class StartInterviewView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "interview/start_interview.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = AnswerForm(request.POST)

        if form.is_valid():

            interview, created = InterviewSession.objects.get_or_create(
                user=request.user,
                completed=False
            )

            answer = form.save(commit=False)
            answer.interview = interview
            answer.question = self.object

            # Evaluate answer using Gemini AI
            score, feedback = evaluate_answer(
                question=self.object.question_text,
                expected_answer=self.object.expected_answer,
                user_answer=answer.user_answer
            )

            # Save AI results
            answer.ai_score = score
            answer.ai_feedback = feedback
            answer.save()

            # Mark interview as completed
            interview.completed = True
            interview.save()

            messages.success(request, "Interview evaluated successfully!")

            return redirect("interview:result", pk=answer.pk)

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class ResultView(LoginRequiredMixin, DetailView):
    model = Answer
    template_name = "interview/result.html"
    context_object_name = "answer"