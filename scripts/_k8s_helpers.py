# _k8s_helpers.py
import subprocess
from pathlib import Path

KUBECTL_AUTO_APPLY = True

# check if kubectl is available
def kubectl_available():
    try: subprocess.run(['kubectl','version','--client'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); return True
    except Exception: return False

# apply k8s yaml content using kubectl
def apply_k8s_yaml(yaml_content, name_hint="auto"):
    tmp = Path(f"/tmp/smart-k8s-{name_hint}.yaml")
    tmp.write_text(yaml_content, encoding='utf-8')
    if KUBECTL_AUTO_APPLY and kubectl_available():
        try:
            subprocess.run(['kubectl','apply','-f',str(tmp)], check=True)
            print(f"✅ Applied k8s YAML: {tmp}")
            return True
        except Exception as e:
            print(f"❌ kubectl apply failed: {e}")
            return False
    else:
        print(f"ℹ️ YAML written to {tmp}")
        return False
    
# create k8s resources from a structured dict assuming keys like SERVICES and DEPLOYMENTS
def create_k8s_from_struct(k8s_obj):
    created = 0
    if not isinstance(k8s_obj, dict): return created
    svcs = k8s_obj.get('SERVICES',[]) + k8s_obj.get('services',[])
    deps = k8s_obj.get('DEPLOYMENTS',[]) + k8s_obj.get('deployments',[])
    for svc in svcs:
        name = svc.get('name') if isinstance(svc, dict) else str(svc)
        port = svc.get('port',80) if isinstance(svc, dict) else 80
        yaml=f"""
apiVersion: v1
kind: Service
metadata:
  name: {name}
spec:
  selector:
    app: {name}
  ports:
    - protocol: TCP
      port: {port}
      targetPort: {port}
"""
        if apply_k8s_yaml(yaml,name_hint=name): created+=1
    for dep in deps:
        name = dep.get('name') if isinstance(dep, dict) else str(dep)
        replicas = dep.get('replicas',1) if isinstance(dep, dict) else 1
        image = dep.get('image','nginx:latest') if isinstance(dep, dict) else 'nginx:latest'
        yaml=f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}-container
        image: {image}
        ports:
        - containerPort: 80
"""
        if apply_k8s_yaml(yaml,name_hint=name): created+=1
    return created
