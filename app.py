import streamlit as st
import boto3
import time
import tempfile
import os

# Initialize the S3 client
aws_access_key = ""
aws_secret_key = ""


# Initialize the S3 client with explicit credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)
# S3 bucket name
bucket_name = 'my-txt-to-csv'

# S3 bucket name


st.title("Text to CSV Converter")

# File upload
uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Upload the file to S3
    s3.upload_file(temp_file_path, bucket_name, uploaded_file.name)
    st.success(f"Uploaded {uploaded_file.name} to S3")

    # Wait for the Lambda function to process the file
    csv_file_key = uploaded_file.name.replace('.txt', '.csv')

    processing = True
    while processing:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv_file:
                csv_file_path = temp_csv_file.name
            s3.download_file(bucket_name, csv_file_key, csv_file_path)
            processing = False
        except Exception as e:
            print(e)
            time.sleep(1)

    st.success(f"Converted {csv_file_key} is ready for download")

    # Provide a download link for the converted CSV file
    with open(csv_file_path, "rb") as f:
        st.download_button(
            label="Download CSV",
            data=f,
            file_name=csv_file_key,
            mime="text/csv"
        )
