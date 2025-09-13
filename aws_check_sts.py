import os, boto3

print("Region (env):", os.getenv("AWS_DEFAULT_REGION"))
try:
    sts = boto3.client("sts", region_name=os.getenv("AWS_DEFAULT_REGION") or "us-east-2")
    ident = sts.get_caller_identity()
    print("✅ STS OK:", ident)
except Exception as e:
    print("❌ STS ERROR:", e)
