import boto3
import csv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    txt_file_key = event['Records'][0]['s3']['object']['key']
    
    # Paths for the temporary files
    txt_file_path = f"/tmp/{os.path.basename(txt_file_key)}"
    csv_file_key = txt_file_key.replace('.txt', '.csv')
    csv_file_path = f"/tmp/{os.path.basename(csv_file_key)}"
    
    try:
        # Download the .txt file from S3
        logger.info(f"Downloading file from S3: s3://{bucket_name}/{txt_file_key}")
        s3.download_file(bucket_name, txt_file_key, txt_file_path)
        logger.info(f"Downloaded file from S3: {txt_file_path}")
        
        # Read the downloaded file and log its content for debugging
        with open(txt_file_path, 'r') as txt_file:
            txt_content = txt_file.read()
            logger.info(f"Content of the downloaded file:\n{txt_content}")

        # Convert .txt file to .csv
        with open(txt_file_path, 'r') as txt_file, open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in txt_file:
                columns = line.strip().split()
                logger.info(f"Writing line to CSV: {columns}")
                writer.writerow(columns)

        # Read the CSV file and log its content for debugging
        with open(csv_file_path, 'r') as csv_file:
            csv_content = csv_file.read()
            logger.info(f"Content of the converted CSV file:\n{csv_content}")
        
        # Verify the file size before uploading
        file_size = os.path.getsize(csv_file_path)
        logger.info(f"CSV file size: {file_size} bytes")

        if file_size > 0:
            # Upload the .csv file to S3
            logger.info(f"Uploading CSV file to S3: s3://{bucket_name}/{csv_file_key}")
            s3.upload_file(csv_file_path, bucket_name, csv_file_key)
            logger.info(f"Uploaded CSV file to S3: s3://{bucket_name}/{csv_file_key}")
        else:
            logger.error("CSV file is empty, not uploading.")
            return {
                'statusCode': 500,
                'body': 'Error: CSV file is empty, not uploaded'
            }

        return {
            'statusCode': 200,
            'body': f'File converted and uploaded to {csv_file_key}'
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
