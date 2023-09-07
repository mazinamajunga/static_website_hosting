import os
import boto3
from botocore.exceptions import NoCredentialsError

def lambda_handler(event, context):
    """
    Lambda function to fetch an object from an S3 bucket, determine if it's an image,
    and respond accordingly.

    Args:
        event (dict): Lambda event input.
        context (object): Lambda context.

    Returns:
        dict: Lambda response containing statusCode, headers, body, and isBase64Encoded.
    """

    # Get the S3 bucket name from the environment variable.
    bucket = os.environ.get('S3_BUCKET')

    # Extract the object key from the Lambda event path.
    key = event['path'].replace('/', '') if event['path'] else 'index.html'

    # Create an S3 client.
    s3 = boto3.client('s3')

    try:
        # Fetch the object from S3.
        response = s3.get_object(Bucket=bucket, Key=key)

        # Extract content type and body from the S3 response.
        content_type = response['ContentType']
        body = response['Body'].read()

        # Initialize variables for base64 encoding and encoding type.
        is_base64_encoded = False
        encoding = 'utf-8'

        # Determine if the content type indicates an image.
        if content_type.startswith('image/'):
            is_base64_encoded = True
            encoding = 'base64'

        # Create the Lambda response.
        resp = {
            'statusCode': 200,
            'headers': {
                'Content-Type': content_type,
            },
            'body': body.decode(encoding),
            'isBase64Encoded': is_base64_encoded,
        }

        return resp

    except NoCredentialsError:
        # Handle AWS credentials not found.
        return {
            'statusCode': 500,
            'body': 'AWS credentials not found.',
        }
    except Exception as e:
        # Handle other exceptions with a 500 status code.
        return {
            'statusCode': 500,
            'body': str(e),
        }
