import unittest
from unittest.mock import MagicMock, patch
# from lambda import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch('boto3.client')
    def test_lambda_handler(self, mock_boto3_client):
        # Mock the S3 response
        mock_s3_response = {
            'ContentType': 'text/html',
            'Body': MagicMock(),
        }

        # Mock the S3 client and its methods
        mock_s3_client = MagicMock()
        mock_s3_client.get_object.return_value = mock_s3_response
        mock_boto3_client.return_value = mock_s3_client

        # Set environment variable
        with patch.dict('os.environ', {'S3_BUCKET': 'my-test-bucket'}):
            event = {
                'path': '/test.html'
            }

            # Invoke the Lambda handler
            result = lambda_handler(event, None)

            # Assert the expected response
            expected_response = {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': mock_s3_response['Body'].decode.return_value,
                'isBase64Encoded': False,
            }
            self.assertEqual(result, expected_response)

    @patch('boto3.client')
    def test_lambda_handler_image(self, mock_boto3_client):
        # Mock the S3 response for an image
        mock_s3_response = {
            'ContentType': 'image/jpeg',
            'Body': MagicMock(),
        }

        # Mock the S3 client and its methods
        mock_s3_client = MagicMock()
        mock_s3_client.get_object.return_value = mock_s3_response
        mock_boto3_client.return_value = mock_s3_client

        # Set environment variable
        with patch.dict('os.environ', {'S3_BUCKET': 'my-test-bucket'}):
            event = {
                'path': '/test.jpg'
            }

            # Invoke the Lambda handler
            result = lambda_handler(event, None)

            # Assert the expected response for an image
            expected_response = {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'image/jpeg',
                },
                'body': mock_s3_response['Body'].read.return_value,
                'isBase64Encoded': True,
            }
            self.assertEqual(result, expected_response)

if __name__ == '__main__':
    unittest.main()
