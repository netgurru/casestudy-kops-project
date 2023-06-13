Creating a Kubernetes cluster with Kops, incorporating multiple instance groups with mixed lifecycle and integrating cluster autoscaler can be achieved by following the steps outlined below.

Architecture Diagram:
```
           +-----------------------+
           |      Load Balancer     |
           +-----------------------+
                         |
           +-----------------------+
           |       Autoscaler       |
           +-----------------------+
                    |       |        
           +-----------------------+
           |  Instance Group (IG1)  |
           +-----------------------+
                    |       |
           +-----------------------+
           |  Instance Group (IG2)  |
           +-----------------------+
                    |       |
           +-----------------------+
           |  Instance Group (IG3)  |
           +-----------------------+
```

Step 1: Create a Kops Cluster Configuration

Create a file named `cluster.yaml` with the following content:
```yaml
apiVersion: kops.k8s.io/v1alpha2
kind: Cluster
metadata:
  name: my-k8s-cluster.example.com
spec:
  api:
    loadBalancer:
      type: Public
  nodeGroups:
  - name: ig1-nodes
    minSize: 1
    maxSize: 5
    instances: # Define the instance types and lifecycle
      - instanceGroupType: mixedInstances
        instances:
          - instanceType: m5.large
            weightedCapacity: 4
            spotPrice: 0.04
            spot: true
          - instanceType: m5.large
            weightedCapacity: 4
            onDemandBaseCapacity: 1
            onDemandPercentageAboveBaseCapacity: 50
  - name: ig2-nodes
    minSize: 1
    maxSize: 5
    instances: # Define the instance types and lifecycle
      - instanceGroupType: mixedInstances
        instances:
          - instanceType: m5.large
            weightedCapacity: 4
            spotPrice: 0.04
            spot: true
          - instanceType: m5.large
            weightedCapacity: 4
            onDemandBaseCapacity: 1
            onDemandPercentageAboveBaseCapacity: 50
  - name: ig3-nodes
    minSize: 1
    maxSize: 5
    instances: # Define the instance types and lifecycle
      - instanceGroupType: mixedInstances
        instances:
          - instanceType: m5.large
            weightedCapacity: 4
            spotPrice: 0.04
            spot: true
          - instanceType: m5.large
            weightedCapacity: 4
            onDemandBaseCapacity: 1
            onDemandPercentageAboveBaseCapacity: 50
```

Step 2: Create the Kubernetes Cluster

Run the following commands to create the Kubernetes cluster using Kops:
```
$ kops create -f cluster.yaml
$ kops update cluster --yes
```

Step 3: Configure Cluster Autoscaler

To enable cluster autoscaler for all instance groups, perform the following steps:

1. Deploy the Cluster Autoscaler:
```yaml
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
```

2. Update the Autoscaler ConfigMap:
```yaml
$ kubectl -n kube-system edit configmap cluster-autoscaler
```
Replace `<OUR CLUSTER NAME>` with the name of our cluster and save the changes.

3. Apply the updated ConfigMap:
```yaml
$ kubectl -n kube-system annotate deployment.apps/cluster-autoscaler cluster-autoscaler.kubernetes.io/safe-to-evict="false"
```

