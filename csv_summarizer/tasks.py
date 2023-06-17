import csv
import time
from celery import shared_task

from core.celery import app as celery_app
from csv_summarizer.models import CSVFile


@shared_task()
def process_csv_file(csv_file_id):
    time.sleep(30)
    csv_files = CSVFile.objects.filter(id=csv_file_id)
    csv_file = csv_files.first()
    if csv_file:
        result = 0
        with open(csv_file.file.path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                row_elements = row[::2]
                for value in row_elements:
                    try:
                        result += int(value)
                    except ValueError:
                        print('The cell contains the wrong data type.')
        return result


def get_task_result(task_id):
    task = celery_app.AsyncResult(task_id)
    if task.ready():
        return task.result


def get_active_tasks_count():
    return 0
