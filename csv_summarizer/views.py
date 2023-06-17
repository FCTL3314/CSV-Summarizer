from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from csv_summarizer.models import CSVFile
from csv_summarizer.serializers import CSVFileSerializer
from csv_summarizer.tasks import (get_active_tasks_count, get_task_result,
                                  process_csv_file)


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
        result = get_task_result(task_id)
        if result is not None:
            return Response(
                {'result': result},
                status=HTTPStatus.OK,
            )
        return Response(
            {'error': 'The task is not yet completed or is missing.'},
            status=HTTPStatus.NOT_FOUND,
        )


class ActiveTasksCountView(APIView):

    @staticmethod
    def get(request):
        count = get_active_tasks_count()
        return Response({'count': count}, status=HTTPStatus.OK)
