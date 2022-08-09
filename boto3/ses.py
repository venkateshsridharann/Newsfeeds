import boto3
import os,sys
from datetime import datetime
from botocore.exceptions import ClientError

date = str(datetime.now())[:10]
year,month,day = date.split("-")

from create_url import *

def send_emails(email_ID): 

    url_dict = create_all_urls()
    dates = []
    links = []
    for x in url_dict:
        
        dates.append(x)
        links.append(url_dict[x])

    SENDER = "vsridharan@privco.com"
    RECIPIENT = email_ID
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "{}/{}/{} - Labeled Newsfeeds".format(month,day,year)

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("-"
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
        <p>Hi Team,<br><br>
        Here are the files for today. <br>
            <a href='{}'>{}</a> <br>
            <a href='{}'>{}</a> <br>
            <a href='{}'>{}</a> <br>
            <a href='{}'>{}</a> <br><br>
            
            Thanks,<br>
            Venkatesh
        </p>
    </body>
    </html>
                """.format(links[0],dates[0],links[1],dates[1],links[2],dates[2],links[3],dates[3])            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent to {}".format(email_ID)),


email_IDs = ['add_emails_here@example.com','add_emails_here2@example.com']

for email in email_IDs:
    send_emails(email)