from flask import Flask, render_template, request
import csv
import boto3

app = Flask(__name__)

# S3 Configuration
S3_BUCKET = "your-bucket-name"
S3_REGION = "us-east-1"
S3_GLACIER_TRANSITION_DAYS = 30  # Number of days to transition to S3 Glacier

# Initialize the S3 client
s3 = boto3.client("s3", region_name=S3_REGION)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_csv", methods=["POST"])
def process_csv():
    # Get the uploaded file
    uploaded_file = request.files["csv_file"]

    # Read and process the CSV file
    csv_content = uploaded_file.read().decode("utf-8")
    csv_lines = csv_content.split("\n")

    # Print content of the lines to the browser
    for line in csv_lines:
        print(line)

    # Upload the CSV file to S3
    s3.upload_fileobj(uploaded_file, S3_BUCKET, uploaded_file.filename)

    # Apply S3 Glacier transition
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=uploaded_file.filename,
        StorageClass="GLACIER",
        Transition={
            "Days": S3_GLACIER_TRANSITION_DAYS,
            "StorageClass": "GLACIER"
        }
    )

    return "CSV file processed and uploaded to S3."


if __name__ == "__main__":
    app.run()
