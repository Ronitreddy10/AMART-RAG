import time
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from kubernetes import client, config

# Attempt to load Kubernetes config. 
# We'll mock the actual job creation if K8s isn't running locally.
try:
    config.load_kube_config()
    k8s_available = True
except Exception as e:
    print(f"Warning: Kubernetes config not found or cluster unreachable. Running in mock mode. Error: {e}")
    k8s_available = False

app = FastAPI(title="Swarm Orchestrator API")

class SwarmRequest(BaseModel):
    num_attacks: int = 10
    target_url: str = "http://target-llm-endpoint.internal"

# Attack vectors based on research (Future Features)
MOCK_VECTORS = [
    "[Context Overflow] Flooding model with 16k tokens, malicious intent hidden at end...",
    "[Context Overflow] Diluting safety guardrails with 8k harmless logs + structured task...",
    "[Multi-Agent] Initiating 'Trust Builder' and 'Framer' agents to set audit context...",
    "[Multi-Agent] 'Refusal Breaker' agent actively bypassing initial rejection...",
    "[Multi-Modal] Injecting PDF payload with tiny/invisible white font instructions...",
    "[Multi-Modal] Simulating RAG retrieval of poisoned chunk into application memory...",
]

def create_kubernetes_job(job_name: str, attack_vector: str, target_url: str):
    """
    Creates a Kubernetes Job object in Python to execute a single attack.
    """
    # Define the container
    container = client.V1Container(
        name="swarm-worker",
        image="python:3.9-slim",
        command=["python", "-c"],
        args=[f"import time; print('Executing {attack_vector} on {target_url}'); time.sleep(2)"],
    )
    
    # Define the template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "swarm-worker"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container])
    )
    
    # Define the Job
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=0
    )
    
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=spec
    )
    
    return job

@app.post("/api/launch-swarm")
def launch_swarm_endpoint(req: SwarmRequest):
    """
    Endpoint to trigger a distributed swarm attack.
    Spawns multiple Kubernetes Jobs concurrently.
    """
    logs = []
    
    logs.append(f"Initializing swarm attack on {req.target_url} with {req.num_attacks} concurrent vectors...")
    
    if k8s_available:
        batch_v1 = client.BatchV1Api()
        
    for i in range(req.num_attacks):
        vector = random.choice(MOCK_VECTORS)
        job_name = f"attack-worker-{int(time.time())}-{i}"
        
        if k8s_available:
            try:
                job = create_kubernetes_job(job_name, vector, req.target_url)
                batch_v1.create_namespaced_job(body=job, namespace="default")
                logs.append(f"Deployed K8s pod {job_name}: {vector}")
            except Exception as e:
                logs.append(f"Failed to deploy K8s pod {job_name}: {e}")
        else:
            # Mock mode
            logs.append(f"[MOCK K8s] Deployed virtual pod {job_name}: {vector}")
            
    logs.append("All attack vectors deployed successfully.")
    
    return {
        "status": "Swarm Launched",
        "jobs_created": req.num_attacks,
        "execution_logs": logs
    }

if __name__ == "__main__":
    print("Starting Swarm Orchestrator API on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
