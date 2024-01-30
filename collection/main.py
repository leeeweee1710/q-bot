import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("http://www.example.com")

ele = driver.find_element(By.CSS_SELECTOR, 'h1')

    # Returns and base64 encoded string into image
ele.screenshot('./image.png')

driver.quit()
  
s3 = boto3.client(
    service_name ="s3",
    endpoint_url = 'https://<accountid>.r2.cloudflarestorage.com',
    aws_access_key_id = '<access_key_id>',
    aws_secret_access_key = '<access_key_secret>',
    region_name="<location>", # Must be one of: wnam, enam, weur, eeur, apac, auto
)

# Get object information
object_information = s3.head_object(Bucket=<R2_BUCKET_NAME>, Key=<FILE_KEY_NAME>)

# Upload/Update single file
s3.upload_fileobj(io.BytesIO(file_content), <R2_BUCKET_NAME>, <FILE_KEY_NAME>)

# Delete object
s3.delete_object(Bucket=<R2_BUCKET_NAME>, Key=<FILE_KEY_NAME>)