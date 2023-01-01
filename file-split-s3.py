import urllib.request, urllib.parse, urllib.error
import json, boto3, os.path
s3 = boto3.client('s3')

def lambda_handler(event,context):
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    copysource = {'Bucket': source_bucket, 'Key': key}
    print("Log is :", context.log_stream_name)
    print("CloudWatch log group name:",  context.log_group_name)
    print("Lambda Request ID:", context.aws_request_id)
    print("Lambda time remaining in MS:", context.get_remaining_time_in_millis())
    try:
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=key)

        #get the file extension
        extention = os.path.splitext(key)[1]

        #copy object to respective folder

        if extention==".pdf":
            s3.copy_object(Bucket="demo-s3-pdf-bucket", Key=key, CopySource=copysource)

        if extention==".jpg":
            s3.copy_object(Bucket="demo-s3-jpg-bucket", Key=key, CopySource=copysource)
        
        if extention==".docx":
            s3.copy_object(Bucket="demo-s3-docx-bucket", Key=key, CopySource=copysource)
        
        if extention==".py":
            s3.copy_object(Bucket="demo-s3-py-bucket", Key=key, CopySource=copysource)
            
    except Exception as e:
        print(e)
        print("error geeting while copying.format not existed")
        raise e