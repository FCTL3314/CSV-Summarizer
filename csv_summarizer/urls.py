from django.urls import path

from csv_summarizer.views import (ActiveTasksCountView, CSVFileView,
                                  TaskResultView)

app_name = 'csv_summarizer'

urlpatterns = [
    path('upload/', CSVFileView.as_view(), name='upload'),
    path('result/<str:task_id>/', TaskResultView.as_view(), name='task-result'),
    path('active-tasks/', ActiveTasksCountView.as_view(), name='active-tasks'),
]
