from src.s3_upload import upload_file

success = upload_file("temp.pdf")

if success:
    print("✅ S3 upload successful!")
else:
    print("❌ S3 upload failed!")