from django.urls import path
from . import views

app_name = "interview"

urlpatterns = [
    path(
        "questions/",
        views.QuestionListView.as_view(),
        name="question_list",
    ),

    path(
        "start/<int:pk>/",
        views.StartInterviewView.as_view(),
        name="start_interview",
    ),

    path(
        "result/<int:pk>/",
        views.ResultView.as_view(),
        name="result",
    ),
]