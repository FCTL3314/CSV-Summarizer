from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from core.celery import app as celery_app
from csv_summarizer.models import CSVFile
from csv_summarizer.serializers import (CSVFileResultSerializer,
                                        CSVFileSerializer)
from csv_summarizer.tasks import get_active_tasks_count, process_csv_file


class CSVFileView(APIView):

    @staticmethod
    def post(request):
        serializer = CSVFileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            csv_file = CSVFile.objects.create(file=file)
            csv_file.save()
            task = process_csv_file.delay(csv_file.id)
            return Response(
                {'task_id': task.id},
                status=HTTPStatus.CREATED,
            )
        return Response(
            serializer.errors,
            status=HTTPStatus.BAD_REQUEST,
        )


class TaskResultView(APIView):

    @staticmethod
    def get(request, task_id):
        task = celery_app.AsyncResult(str(task_id))
        if task.ready():
            result = task.result
            serializer = CSVFileResultSerializer({'result': result})
            return Response(serializer.data, status=HTTPStatus.OK)
        else:
            return Response({'detail': 'Task is still in progress.'}, status=HTTPStatus.ACCEPTED)


class ActiveTasksCountView(APIView):

    @staticmethod
    def get(request):
        return Response({'count': get_active_tasks_count()}, status=HTTPStatus.OK)
