import boto3
from picon.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION

key_id = AWS_ACCESS_KEY_ID
secret_key = AWS_SECRET_ACCESS_KEY
bucket_name = AWS_STORAGE_BUCKET_NAME
region = AWS_REGION
s3 = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key
    )


def create_s3_bucket(bucket_):
    try:
        response = s3.create_bucket(
            Bucket='com-noc-picon',
            CreateBucketConfiguration={
                'LocationConstraint': AWS_REGION
            },
        )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Bucket already exists. skipping..")
        else:
            print("Unknown error, exit..")
