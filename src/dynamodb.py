import uuid
from datetime import datetime

import boto3

TABLE_NAME = "DocuSenseDocuments"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def save_document_metadata(
    filename,
    language,
    document_type,
    s3_key
):
    """
    Save uploaded document metadata to DynamoDB.
    """

    document_id = str(uuid.uuid4())

    item = {
        "document_id": document_id,
        "filename": filename,
        "language": language,
        "document_type": document_type,
        "s3_key": s3_key,
        "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    table.put_item(Item=item)

    print("✅ Metadata saved to DynamoDB")

    return document_id