from django.urls import path

from csv_summarizer.views.api_views import (ActiveTasksCountView, CSVFileView,
                                            TaskResultView)

app_name = 'csv_summarizer'

urlpatterns = [
    path('upload/', CSVFileView.as_view(), name='upload'),
    path('result/<uuid:task_id>/', TaskResultView.as_view(), name='task-result'),
    path('active-tasks/', ActiveTasksCountView.as_view(), name='active-tasks'),
]
