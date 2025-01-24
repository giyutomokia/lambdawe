import json
import base64
import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Retrieve the base64-encoded file content and metadata from the event
    bucket_name = event.get("bucket_name")
    file_name = event.get("file_name")
    file_data_base64 = event.get("file_data")

    # Decode the base64-encoded file data
    try:
        file_data = base64.b64decode(file_data_base64)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Failed to decode base64 file data',
                'details': str(e)
            })
        }

    # Upload the file to the specified S3 bucket
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_data,
            ContentType='application/pdf'  # You can adjust this for other file types if necessary
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'File {file_name} uploaded successfully to {bucket_name}.'
            })
        }
    except NoCredentialsError:
        return {
            'statusCode': 403,
            'body': json.dumps({
                'error': 'AWS credentials not found or invalid.'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to upload file to S3',
                'details': str(e)
            })
        }
