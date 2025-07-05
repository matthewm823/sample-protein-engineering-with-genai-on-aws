import boto3

def wait_for_s3_file(bucket_name, key, max_attempts=60, delay=5):
    """
    Use boto3's built-in waiter to wait for S3 object
    """
    s3_client = boto3.client('s3')
    
    waiter = s3_client.get_waiter('object_exists')
    
    try:
        waiter.wait(
            Bucket=bucket_name,
            Key=key,
            WaiterConfig={
                'Delay': delay,
                'MaxAttempts': max_attempts
            }
        )
        print(f" File {key} is available")
        return True
    except Exception as e:
        print(f" Timeout waiting for {key}: {e}")
        return False
