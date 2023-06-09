# casestudy-kops-project
Project for showcase of case study for Kubernetes based Project

## Description
To create a Kubernetes cluster creation configuration for kops with multiple instance groups, mixed instance groups, and lifecycle configurations (spot and on-demand), along with the cluster autoscaler enabled for all instance groups. Please follow the example below:
In this example, I have defined three instance groups: ondemand-group, spot-group, and mixed-group. Each group specifies the minimum and maximum size, instance configurations, subnets, and the instance lifecycle (On-Demand or Spot). The mixed group includes a combination of On-Demand and Spot instances.
Additionally, I have included the necessary IAM policies for autoscaling to work correctly. The clusterAutoscaler section enables the cluster autoscaler for all instance groups, with some configuration options like utilization thresholds and scan intervals.

Please note that you may need to adjust the instance types, AMIs, regions, and other parameters according to your specific requirements and environment.

Once you have created the configuration file, you can use kops to create the cluster using the following command:
`
kops create -f cluster-config.yaml
`

### INFRA
To achieve the requirements mentioned, follow the steps below:

Step 1: Create a Deployment with Nginx and the web application:

Create a file named `deployment.yaml` and add the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-webapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-webapp
  template:
    metadata:
      labels:
        app: nginx-webapp
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - name: shared-files
              mountPath: /usr/share/nginx/html
        - name: webapp
          image: your-web-application-image
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: shared-files
              mountPath: /usr/share/nginx/html
      volumes:
        - name: shared-files
          emptyDir: {}
```

Replace `your-web-application-image` with the actual image of your web application.

Step 2: Expose the application with a Service:

Create a file named `service.yaml` and add the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-webapp-service
spec:
  selector:
    app: nginx-webapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

This will expose the service using a LoadBalancer type, which can be accessed externally.

Step 3: Implement autoscaling for the Deployment:

To implement autoscaling, you can use Kubernetes Horizontal Pod Autoscaler (HPA). Modify the `deployment.yaml` file to add the HPA configuration:

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-webapp-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-webapp
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

This configuration sets the minimum number of replicas to 1 and the maximum to 5. It also specifies that autoscaling should be based on CPU utilization, targeting an average utilization of 50%.

Step 4: Use Helm to render Kubernetes objects for reusability:



Helm is a package manager for Kubernetes that allows you to create reusable templates for Kubernetes objects. To use Helm, follow these steps:

1. Install Helm on your machine by following the Helm installation guide (https://helm.sh/docs/intro/install/).

2. Initialize Helm:

   ```bash
   helm init
   ```

3. Create a Helm chart structure:

   ```bash
   helm create mychart
   ```

4. Navigate to the chart directory:

   ```bash
   cd mychart
   ```

5. Modify the generated `values.yaml` file to set your desired values for the deployment, service, and autoscaling.

6. Create templates for the Deployment and Service in the `templates` directory. You can use the existing YAML files or split them into smaller template files.

7. Render the Kubernetes objects using Helm:

   ```bash
   helm template mychart/
   ```

   This will generate the rendered YAML files based on your Helm chart.

You can customize the Helm chart and templates based on your specific needs.

That's it! You now have a deployment with Nginx and a web application running in the same pod, sharing public files through shared storage. The application is exposed with a Service object, and autoscaling is implemented. Ansible is used for basic configuration management, and Helm is used to render Kubernetes objects for reusability.


### DEVELOPMENT

Sure! I can help you with that. Here's an example of a web application using Python and Flask framework to parse and process CSV files, upload them to S3 storage, and implement S3 Glacier transition.

First, make sure you have Flask and Boto3 (AWS SDK for Python) installed. You can install them using pip:

```
pip install flask boto3
```

Next, create a new Python file, for example, `app.py`, and add the following code:

```python
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
```

In this code, we define the Flask routes for the homepage (`/`) and the CSV processing endpoint (`/process_csv`). The `/` route renders an HTML template called `index.html`, which you need to create in a `templates` folder in the same directory as `app.py`.

Create the `templates/index.html` file and add the following HTML code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>CSV Processor</title>
</head>
<body>
    <h1>CSV Processor</h1>
    <form action="/process_csv" method="post" enctype="multipart/form-data">
        <input type="file" name="csv_file" accept=".csv" required>
        <button type="submit">Upload and Process</button>
    </form>
</body>
</html>
```

Make sure to replace `"your-bucket-name"` with your actual S3 bucket name. Also, adjust the `S3_REGION` if your bucket is located in a different region.

To run the web application, execute the following command in your terminal:

```
python app.py
```

The application will start, and you can access it in your web browser at `http://localhost:5000`. You'll see a simple interface with an option to upload a CSV file.

When you upload a CSV file, it will be processed and the content of each line will be printed to the browser. The file will also be uploaded to your S3 bucket, and the S3 Glacier transition will be applied to the uploaded file.

Remember to have your AWS credentials properly configured on your machine. You can use the AWS CLI or set the environment variables (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) for authentication.

Please note that this is a basic example to get you started. You can extend the functionality and improve error handling as needed.
