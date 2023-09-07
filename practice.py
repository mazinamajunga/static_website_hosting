import boto3

S3_BUCKET = "mynewestfirstbucket"
KEY = "copy_file1.txt"
# s3 = boto3.resource('s3')

# bucket = s3.Bucket('S3_BUCKET')
# for obj in bucket.objects.all():
#     print(obj.key)
    
s3 = boto3.client('s3')
response = s3.get_object(Bucket=S3_BUCKET, Key=KEY)
print(response)
# for obj in s3.get(S3_BUCKET):
#     print(obj.key)