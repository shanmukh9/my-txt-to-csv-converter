import boto3
import csv
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    txt_file_key = event['Records'][0]['s3']['object']['key']
    
    # Download the .txt file from S3
    txt_file_path = f"/tmp/{os.path.basename(txt_file_key)}"
    s3.download_file(bucket_name, txt_file_key, txt_file_path)
    
    # Convert .txt file to .csv
    csv_file_key = txt_file_key.replace('.txt', '.csv')
    csv_file_path = f"/tmp/{os.path.basename(csv_file_key)}"
    
    with open(txt_file_path, 'r') as txt_file, open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for line in txt_file:
            writer.writerow(line.strip().split())
    
    # Upload the .csv file to S3
    s3.upload_file(csv_file_path, bucket_name, csv_file_key)
    
    return {
        'statusCode': 200,
        'body': f'File converted and uploaded to {csv_file_key}'
    }
