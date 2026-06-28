import os
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError

BUCKET_NAME = "docusense-storage-navodya"

s3 = boto3.client("s3")


def upload_file(file_path, object_name=None):

    if object_name is None:

        filename = os.path.basename(file_path)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        object_name = f"{timestamp}_{filename}"

    try:
        s3.upload_file(file_path, BUCKET_NAME, object_name)

        print(f"✅ Uploaded '{object_name}' to S3.")

        return object_name

    except FileNotFoundError:
        print("❌ File not found.")
        return None

    except NoCredentialsError:
        print("❌ AWS credentials not found.")
        return None

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None