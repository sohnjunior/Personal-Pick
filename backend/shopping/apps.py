from django.apps import AppConfig
from django.conf import settings
# import boto3
# from io import BytesIO


class ShoppingConfig(AppConfig):
    name = 'shopping'
    # model_params = None
    #
    # def ready(self):
    #     """
    #     앱 초기화시 필요한 작업들을 수행한다.
    #
    #     :return: None
    #     """
    #     # create s3 client
    #     s3client = boto3.client('s3',
    #                             aws_access_key_id=settings.S3_ACCESS_KEY,
    #                             aws_secret_access_key=settings.S3_SECRET_KEY)
    #
    #     # get objects from s3 /w hints
    #     response = s3client.get_object(Bucket='personal-pick', Key='model/deep.pt')
    #     print('load necessary files from s3')
    #
    #     # read data from s3
    #     body = response['Body'].read()
    #     stream = BytesIO(body)
    #     ShoppingConfig.model_params = stream
    #     print(f'read model params data from s3')
