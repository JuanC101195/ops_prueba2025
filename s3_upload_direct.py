import os, boto3, botocore

bucket = os.getenv("S3_BUCKET")
region = os.getenv("AWS_DEFAULT_REGION") or "us-east-2"

print("Bucket:", bucket)
print("Region:", region)

s3 = boto3.client("s3", region_name=region)
# Subimos con key simple, sin prefijo
s3.upload_file("sample_data/ejemplo.txt", bucket, "ejemplo.txt")
print("✅ Subida directa OK: s3://%s/%s" % (bucket, "ejemplo.txt"))
