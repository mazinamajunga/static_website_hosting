# import os
# import boto3
# from botocore.exceptions import NoCredentialsError

# def lambda_handler(event, context):
#     """
#     Lambda function to fetch an object from an S3 bucket, determine if it's an image,
#     and respond accordingly.

#     Args:
#         event (dict): Lambda event input.
#         context (object): Lambda context.

#     Returns:
#         dict: Lambda response containing statusCode, headers, body, and isBase64Encoded.
#     """

#     # Get the S3 bucket name from the environment variable.
#     bucket = os.environ.get('S3_BUCKET')

#     # Extract the object key from the Lambda event path.
#     key = event['path'].replace('/', '') if event['path'] else 'index.html'

#     # Create an S3 client.
#     s3 = boto3.client('s3')

#     try:
#         # Fetch the object from S3.
#         response = s3.get_object(Bucket=bucket, Key=key)

#         # Extract content type and body from the S3 response.
#         content_type = response['ContentType']
#         body = response['Body'].read()

#         # Initialize variables for base64 encoding and encoding type.
#         is_base64_encoded = False
#         encoding = 'utf-8'

#         # Determine if the content type indicates an image.
#         if content_type.startswith('image/'):
#             is_base64_encoded = True
#             encoding = 'base64'

#         # Create the Lambda response.
#         resp = {
#             'statusCode': 200,
#             'headers': {
#                 'Content-Type': content_type,
#             },
#             'body': body.decode(encoding),
#             'isBase64Encoded': is_base64_encoded,
#         }

#         return resp

#     except NoCredentialsError:
#         # Handle AWS credentials not found.
#         return {
#             'statusCode': 500,
#             'body': 'AWS credentials not found.',
#         }
#     except Exception as e:
#         # Handle other exceptions with a 500 status code.
#         return {
#             'statusCode': 500,
#             'body': str(e),
#         }





















import json
import boto3
import os

# Create an S3 client using Boto3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda function to retrieve an object from an S3 bucket and return it as an HTTP response.
    
    Args:
        event (dict): Event data passed to the Lambda function.
        context (object): Lambda function runtime information.

    Returns:
        dict: A dictionary containing the HTTP response data.
    """

    # Get the name of the S3 bucket from an environment variable
    bucket = os.environ['S3_BUCKET']

    # Extract the object key from the request path
    key = event['path'].lstrip('/')

    # If the key is empty, set it to 'index.html'
    if not key:
        key = 'index.html'

    try:
        # Retrieve the object from S3
        response = s3.get_object(Bucket=bucket, Key=key)

        # Extract the content type of the object
        content_type = response['ContentType']

        # Check if the content type indicates binary (image) data
        is_base64_encoded = content_type.startswith('image/')

        # Read the object's body and encode it as base64 if it's binary, otherwise decode it as UTF-8
        if is_base64_encoded:
            body = response['Body'].read().encode('base64')
        else:
            body = response['Body'].read().decode('utf-8')

        # Create and return an HTTP response dictionary
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': content_type,
            },
            'body': body,
            'isBase64Encoded': is_base64_encoded
        }
    except Exception as e:
        # Handle any exceptions and return an error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


