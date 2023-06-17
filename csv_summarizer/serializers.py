from rest_framework import serializers

from csv_summarizer.models import CSVFile


class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = ('file',)
