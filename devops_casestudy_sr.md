K8s Cluster (not expecting to have running cluster):
 - We are asking you to create Kubernetes cluster creation config for kops which has multiple ig, mixed instance group and lifecycle (spot and ondemand).
 - Have cluster autoscaler for all instance groups

Infra: 
 - Create deployment which contains Nginx and below web application running (within same pod) and sharing public files (css, js etc) through shared storage (not nfs). 
 - Expose application with creating service object.
 - Implement auto scaling for deployment.
 - Implementing/using basic configuration management with Ansible (to have application configs in Ansible) 
 - Use helm to render Kubernetes objects for re-using while creating new environments
 
Development:
  - Develop a basic web application (using Python, Node.js or Go) to parse and process CSV files like attached format. When processing file you can just print content of the lines to browser.
  - Web application should has basic interface to upload CSV and show peviously processed files.
  - Once CSV file processed upload it to the s3 storage. 
  - Waiting you to implement s3 glacier transition on s3 config.

Notes:
  - You can use Minukube to deploy application locally
  - You can use dockerhub to store Docker images
  - You can use github to store application and infra codes

Attachment: soh.csv

Solutioning:
  - Documentation and architecture diagram
