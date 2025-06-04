from kubernetes import client, config
import os

def list_pods():
    try:
        # Use in-cluster config if running inside K8s
        config.load_incluster_config()
        namespace = os.getenv("POD_NAMESPACE", "default")
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace=namespace)

        return [{"name": pod.metadata.name, "status": pod.status.phase} for pod in pods.items]
    except Exception as e:
        return {"error": str(e)}
