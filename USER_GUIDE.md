# User guide

- I've used k3s inside of WSL for the local dev environment.
- I've started the registry inside of the k3s manually and port-forwarded it to push the images from local terminal
    - kubectl create namespace registry
    - kubectl run registry --image=registry:2 --port=5000 -n registry
    - kubectl expose pod registry --port=5000 --target-port=5000 --name=registry -n registry
    - REGISTRY_IP=$(kubectl get svc registry -n registry -o jsonpath='{.spec.clusterIP}')
    - sudo bash -c "echo '$REGISTRY_IP registry' >> /etc/hosts"
    - kubectl port-forward svc/registry 5000:5000 -n registry
- I've also port-forwarded the application itself to test it.
    - kubectl port-forward svc/myapp 8080:80 -n production
    - ./app/test_requests.sh