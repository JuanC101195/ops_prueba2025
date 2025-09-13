import boto3, os
try:
    sts = boto3.client("sts", region_name=os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    print(sts.get_caller_identity())
    print("⚠️ Aún hay credenciales activas")
except Exception as e:
    print("✅ Sin acceso a AWS con las credenciales actuales:", e)
