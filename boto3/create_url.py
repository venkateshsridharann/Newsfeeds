import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta


def create_presigned_url(date):

    # Generate a presigned URL for the S3 object
    try:
        bucket_name = 'privco-newsfeeds'
        database_file = 'database_{}_.csv'.format(date)
        object_name = 'database_labeled/'+database_file
        response = boto3.client('s3').generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=18000)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response

def create_all_urls():
    today = datetime.today()
    one_day_before = today - timedelta(days=1)
    two_day_before = today - timedelta(days=2)
    three_day_before = today - timedelta(days=3)

    today = str(today)[:10]
    one_day_before = str(one_day_before)[:10]
    two_day_before = str(two_day_before)[:10]
    three_day_before = str(three_day_before)[:10]


    urls = {}
    urls[today] = create_presigned_url(today)
    urls[one_day_before] = create_presigned_url(one_day_before)
    urls[two_day_before] = create_presigned_url(two_day_before)
    urls[three_day_before] = create_presigned_url(three_day_before)

    return urls
