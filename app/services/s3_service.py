import boto3
from fastapi import HTTPException

class S3Service:
    def __init__(self, aws_access_key: str, aws_secret_key: str, aws_region: str, bucket_name: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        self.bucket_name = bucket_name
    
    def generate_presigned_url(self, file_name: str, file_type: str, expiration: int = 3600) -> dict:
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    "Key": file_name,
                    "ContentType": file_type
                },
                ExpiresIn=expiration
            )
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            return {"presignedUrl": presigned_url, "fileUrl": file_url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")
