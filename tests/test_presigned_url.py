import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from app.services.s3_service import S3Service
from app.core.config import settings

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_KEY = settings.AWS_SECRET_KEY
AWS_REGION = settings.AWS_REGION

BUCKET_NAME = settings.S3_BUCKET_NAME

s3_service = S3Service(
    aws_access_key=AWS_ACCESS_KEY,
    aws_secret_key=AWS_SECRET_KEY,
    aws_region=AWS_REGION,
    bucket_name=BUCKET_NAME
)

def test_generate_presigned_url():
    try:
        test_file_name = "test-image.jpg"
        test_file_type = "image/jpeg"
        
        response = s3_service.generate_presigned_url(
            file_name=test_file_name,
            file_type=test_file_type,
        )

        presigned_url = response["presignedUrl"]
        file_url = response["fileUrl"]

        assert presigned_url is not None, "Presigned URL is None"
        assert file_url is not None, "File URL is None"

        print("Presigned URL:", presigned_url)
        print("File URL:", file_url)

        test_file_path = "tests/data/test-image.jpg"
        with open(test_file_path, "rb") as file:
            upload_response = s3_service.s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=test_file_name,
                Body=file,
                ContentType=test_file_type,
            )

        assert upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200, "Failed to upload file via Presigned URL"
        print("File uploaded successfully!")

    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credential Error: {e}")
        assert False, "AWS Credentials are invalid"
    except Exception as e:
        print(f"Test failed: {e}")
        assert False, "Presigned URL generation test failed"

if __name__ == "__main__":
    test_generate_presigned_url()     
