import os
import boto3
import logging
from botocore.exceptions import ClientError

def upload_previous_to_aws(date):
    date = date[:-3]
    try:
        if os.path.isfile('../tmp/previously_seen_{}.csv'.format(date)):
            prev_file = 'previously_seen_{}.csv'.format(date)
            previously_seen = open("../tmp/"+prev_file, 'rb')
            boto3.resource('s3').Bucket('aws-venky-newsfeeds').put_object(Key='previous/'+prev_file, Body=previously_seen)
            print(prev_file+' File  uploaded\n')

    except Exception as e:
        print(e)
        print('error while uploading previously seen\n')

def upload_database_to_aws(date):
    try:
        if os.path.isfile('../tmp/database_{}.csv'.format(date)):
            database_file = 'database_{}.csv'.format(date)
            database = open("../tmp/"+database_file, 'rb')
            boto3.resource('s3').Bucket('aws-venky-newsfeeds').put_object(Key='database/'+database_file, Body=database)
            print(database_file+' File  uploaded\n')
    
    except Exception as e:
        print(e)
        print('error while uploading database\n')


def upload_labeled_database_to_aws(date):
    try:
        if os.path.isfile('../tmp/database_{}_.csv'.format(date)):
            database_file = 'database_{}_.csv'.format(date)
            database = open("../tmp/"+database_file, 'rb')
            boto3.resource('s3').Bucket('aws-venky-newsfeeds').put_object(Key='database_labeled/'+database_file, Body=database)
            print(database_file+' labeled file  uploaded\n')
    
    except Exception as e:
        print(e)
        print('error while uploading database\n')


def upload_bankruptcy_ipo_to_aws(date):
    try:
        if os.path.isfile('../tmp/bankruptcy_ipo_{}.csv'.format(date)):
            database_file = 'bankruptcy_ipo_{}.csv'.format(date)
            database = open("../tmp/"+database_file, 'rb')
            boto3.resource('s3').Bucket('aws-venky-newsfeeds').put_object(Key='bankruptcy_ipo/'+database_file, Body=database)
            print(database_file+' File  uploaded\n')
    
    except Exception as e:
        print(e)
        print('error while uploading bankruptcy\n')

def remove_from_local(date):

    if os.path.isfile('../tmp/database_{}.csv'.format(date)):
        os.remove('../tmp/database_{}.csv'.format(date))  
        print('database_{}.csv'.format(date)+' File  removed\n')

    if os.path.isfile('../tmp/database_{}_.csv'.format(date)):
        os.remove('../tmp/database_{}_.csv'.format(date))  
        print('database_{}_.csv'.format(date)+' File  removed\n')

    if os.path.isfile('../tmp/previously_seen_{}.csv'.format(date[:-3])):
        os.remove('../tmp/previously_seen_{}.csv'.format(date[:-3]))
        print('previously_seen_{}.csv'.format(date)+' File  removed\n')

    if os.path.isfile('../tmp/bankruptcy_ipo_{}.csv'.format(date)):
        os.remove('../tmp/bankruptcy_ipo_{}.csv'.format(date))
        print('bankruptcy_ipo_{}.csv'.format(date)+' File  removed\n')
    
 

def upload_to_s3(date):
    upload_database_to_aws(date)
    upload_labeled_database_to_aws(date)
    upload_bankruptcy_ipo_to_aws(date)
    upload_previous_to_aws(date)
    remove_from_local(date)
    
    
