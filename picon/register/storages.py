from django.core.files.storage import Storage
import requests
from picon import settings


class S3Storage(Storage):

    def delete(self, file_name):
        path = f'http://{AWS_S3_CUSTOM_DOMAIN}'
        url = f'{path}/{file_name}'
        response = requests.delete(url, )
        return response == 204
