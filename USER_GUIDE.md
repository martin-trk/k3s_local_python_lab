# User guide

## Local development environment

- I've used **k3s inside WSL** as the local Kubernetes environment.
- To run the application locally, copy the local GitLab CI job configuration and execute it with `LOCAL_RUN=true`.
- The job will automatically:
  - Create the local container registry inside k3s.
  - Expose it through a NodePort.
  - Configure the required image variables.
  - Build and push the application image.
  - Deploy the application through Terraform.

### Local registry setup

Copy the `setup_local_registry` job from the GitLab CI configuration, and the commands of that, it will able to use everything dynamically.