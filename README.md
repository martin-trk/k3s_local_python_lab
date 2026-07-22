# DevOps Engineer Homework

## Overview

The goal of this assignment is to evaluate how you approach a typical DevOps engineering task involving:

- Application development / scripting
- Containerization
- Kubernetes
- Helm
- Terraform
- CI/CD
- Code review

The repository contains intentionally incomplete and imperfect components.
Your task is to complete, improve and document the solution.

You are not expected to produce a perfect production-ready system. We are more interested in your engineering approach, decision-making and ability to balance quality with the time constraints.

Time limit: approximately **3 hours**

## Repository Contents

The repository contains:

- An incomplete application skeleton
- Terraform configuration requiring review and improvement
- An incomplete Helm chart
- An incomplete CI/CD pipeline

Your task is to complete and improve these components. Our goal is to understand your engineering approach, and we will build the upcoming technical interview on this project.

## Goal 1

Complete and improve the provided project.

The repository contains the following files:

- Incomplete application code
- Broken/incomplete terraform configuration
- Incomplete Helm Chart
- Incomplete Gitlab CI pipeline

### Requirements

#### Application

Implement a simple application in either:

- Go
- Python

The application must expose the following endpoints:

##### `GET /health`

**Response:**

```json
{
    "status": "ok"
}
```

##### `GET /version`

**Response:**

```json
{
    "version": "1.0.0"
}
```

##### `GET /env`

**Response:**

```json
{
    "environment": "<value from ENVIRONMENT variable>"
}
```

##### `POST /config`

**Request:**

```json
{
    "name": "database_url",
    "value": "postgres://example"
}
```

**Response:**

```json
{
    "name": "database_url",
    "value": "postgres://example"
}
```

##### `GET /config/{name}`

**Example:**

```bash
GET /config/database_url
```

**Response:**

```json
{
    "name": "database_url",
    "value": "postgres://example"
}
```

##### `DELETE /config/{name}`

**Response:**

```json
{
    "deleted": true
}
```

#### Containerization

- Create the necessary Dockerfile with minimal setup
- The image should:
  - build successfully
  - run locally
  - expose the application endpoint

#### Terraform

- Review and fix/complete the Terraform code
- The Terraform code contains several issues and areas for improvement
- In case you don't get time to implement changes describe what would you still improve and why
- Document any changes you make

#### Helm

- Review and fix/complete the Helm Chart
- The chart should deploy the application to Kubernetes
- Document any change you make

#### Gitlab CI

- Complete the pipeline so it becomes capable of building and deploying the application
- The pipeline should support the workflow required to build and deploy the application
- The pipeline should be logically complete and demonstrate how you would automate the process
- Add any other necessary jobs to the pipeline

#### Documentation

Update the project README with following information.

##### What You Changed

###### Application

I've drafted a really basic Python application with all the six required endpoints. Apart from that I've created a test_requests.sh which could be polished more, I was generating it for my testing.

Created a minimal Dockerfile which can run the `app.py` and exposing it to the proper port.

As for me, it wasn't the focus to create a perfect application.

###### Helm

Fixed three deploy-blocking bugs:
- There was a mismatch on the service selector (`myapp` vs `myapps`)
- Ingress was pointing to the wrong service (`homeworks` vs `myapp`)
- Container port mismatch (`5000` vs `8080`)

###### Terraform

- Fixed broken `set` blocks in `main.tf` (missing value, missing `=`, unsupported multiple set blocks)
- Missing `=` in the Helm provider's Kubernetes config block
- Fixed the `chart` value of the Helm chart, removed the part of `/homework`, the folder structure was prepared without it.
- Changed the `kube_config_path` due to that I was using k3s and had a different path by default. But this may differ for different environments/Kubernetes platforms/configurations
- Added `tfvars/prod_terraform.tfvars` for prod values
- Replaced hardcoded variables and ingested the variable created in `variables.tf`
- Added one more variable (`image.repository`) to the Terraform configuration and used it in the `main.tf` to be able to overwrite default Helm values in case of multiple sources (I was switching from local copied images to local, k3s based registry)
- Realized some warnings regarding deprecated resource name
    - Replaced `kubernetes_namespace` -> `kubernetes_namespace_v1` on both places

###### Gitlab CI

- Added a Docker build and push job
- Added a shared `terraform_setup` anchor which is used by all the Terraform jobs
- Splitted `deploy` job into Terraform `plan` and `apply`
- Added `destroy` jobs in case of environment clean-up, especially in local environments
- Gated the `destroy` job behind `CONFIRM_TO_DESTROY` variable, only appears if it is added
- Added a local-only job for copy-pasting pipeline variables which are not present by default when testing it locally
- Implemented Terraform plan job with plan file to prevent unneeded changes. ~~Identical file creation with the value with combining pipeline ID and the pipeline start time stamp~~
    - Removed the date identifier to prevent inconsistencies
- Adding multiple TF Vars mapped with branching strategy similar to GitFlow
    - The job is getting the tfvar based on the branch we are running the pipeline
    - `develop` branch -> develop environment
    - RC tags (`v1.2.3-rc1`, `v1.2.3-rc.1`, etc.) -> preprod environment
    - Release tags (`v1.2.3`) -> prod environment

##### Assumptions

- Local k3s is an acceptable target without any cloud deployment
- I've looked at this assessment as something which we can apply for an already existing environment, "import compatible" project, not something which should be up and running by any "1 click" script on local dev environments. So my assumption is that there is already a Kubernetes cluster somewhere, and a container registry running somewhere (I've started mine manually on the k3s cluster) with ready-to-work network on some level.
- My assumption was that its not a problem if I focus more on the GItlab CI, Terraform, Helm and the documentation. The application is a really minimal one which can pass the requirements, but no more, and it is definetely something I wouldn't take it as my best effort task. But had to take the decision because of the time limitation.

##### Known Limitations

- Gitlab-CI-Local unverified - spent about ~1-1.5 hours on local networking/permission errors with gitlab-ci-local and I let it go as a local-tooling issue. Config is committed as-is.
- As a result I was not able test properly the Gitlab CI yml file.
- I can clearly imagine that there is a syntax error or something which could not match in a real Gitlab pipeline and it would throw an error on.
- I've put the main focus more like on the Gitlab CI, Terraform, and properly documented most of the things, my focus was not on application development, the application is a really minimal one which can complete the requirements, but it is definetely something I wouldn't take it as my best effort task. But had to take the decision because of the time limitation. **So the application is definetely something which is a known limitation.**
- No proper networking. Due to the time limit, I couldn't complete more on the networking related part. I was just using port-forward to test my application.
- There isn't any "1 click" start to the platform to start up the dev environment for this assessment.


##### Production Improvements

- Definetely a better application along with tests for the application
- If the application is more robust with multiple files, classes, and even we need to compile it, the multi staged Dockerfiles should be used with hardening steps, or use something like Buildpacks, which can support building Docker images easier with the help of a command and some configuration (hardening, multi layer, but also harder to troubleshoot)
- Proper image tagging mechanism
- More robust Kubernetes deployment and with other existing cloud resources supporting it, if the goal would be to deploy it on cloud (ACR for the images, AKS for the cluster, at least one AppGW, managed identites, etc)
- More robust Helm chart on the deployment (resources, liveness/readiness probe, etc...)
- Proper Terraform backend with a cloud storage with locking, storing the state, etc
- ~~Better ruled Gitlab CI Jobs matched with the branching/releasing strategy what the team uses~~
    - Started to implement but there are still room for improvement, of course
    - For example, improve on adding a rule to be able to back up any environment based on tags. So if the dev environment got broken, we are able to deploy dev from tags, bot not the opposite way.
- Templatized Gitlab CI Jobs can be also useful with tagged or hashed version of the template
- Pre-Jobs, gates on the pipeline (Linting, Security checks -PW checking, scanning-, Unit test, etc)
- Pre commit hooks for preventing the Helm and/or Terraform syntax errors, if it is applicable for the environment
- Some kind of test after the pipeline run, even maybe a rollback solution if the test is passed. (both for the application and the infrastructure)
- In a real Gitlab repo, I wouldn't commit directly to main, of course. 

##### User guide

- I've used k3s inside of WSL for the local dev environment, so a small working kubernetes cluster with ready to use kubectl config is expected
- I've started the registry inside of the k3s manually and port-forwarded it to push the images from local terminal
    - `kubectl create namespace registry`
    - `kubectl run registry --image=registry:2 --port=5000 -n registry`
    - `kubectl expose pod registry --port=5000 --target-port=5000 --name=registry -n registry`
    - `REGISTRY_IP=$(kubectl get svc registry -n registry -o jsonpath='{.spec.clusterIP}')`
    - `sudo bash -c "echo '$REGISTRY_IP registry' >> /etc/hosts"`
    - `kubectl port-forward svc/registry 5000:5000 -n registry`
- All the Gitlab CI job commands are prepared for ready to paste from the script section to the local terminal (I was also used like that due to not having local Gitlab runners, didn't have time to complete that)
    - `variable-set-job-for-local-test`: Copy and paste the whole `script` section after the pipe to import all variables
    - `docker-build-and-push`: Feel free to also copy and paste the commands. 
    - `terraform_plan`: For that, first you need to paste the `.terraform_setup` anchor commands, after that you can run the plan command.
        - `cd ${TF_ROOT}`
        - `terraform init`
        - `terraform validate`
        - `terraform plan -var-file=${TF_VARS_FILE} -out=${TF_PLAN_FILE}`
    - `terraform_apply`: Moving along to the apply, ready to paste the command
    - `terraform_destroy_plan` and `terraform_destroy_apply`
        - These protected with a variable `$CONFIRM_TO_DESTROY == "true"`
        - `export CONFIRM_TO_DESTROY=true`
- I've also port-forwarded the application itself to test it.
    - `kubectl port-forward svc/myapp 8080:80 -n production`
    - `./app/test_requests.sh`

### Deliverables

- Source Code of the Go/Python application
- Dockerfile
- Terraform changes
- Helm changes
- CI pipeline changes
- README describing decisions, assumptions and user guide for the project.

### Notes

You are not expected to deploy to a cloud provider.
The solution should work with a local Kubernetes cluster such as:

- Kind
- Minikube
- K3d

### Timing

Timebox yourself to approximately **3 hours**. If you can't finish the work within the timebox, describe in the README.md what is left and how you would approach it.

## Goal 2

You get this half-baked project from one of your colleagues who is a Junior and asking for your guidance.

Provide a short code review in `REVIEW.md` where you address the **top 5 most important things** to fix so the colleague can move forward.

### Review Timing

Spend no more than **30 minutes** on review and feedback.

### Evaluation Criteria

We will evaluate:

- Code quality
- Terraform quality
- Kubernetes and Helm knowledge
- CI/CD design and implementation
- Documentation quality
- Code review quality
- Maintainability and operational thinking

### Use of AI

The use of AI-assisted tools is permitted. However, we encourage you to complete the assignment primarily based on your own knowledge, experience and reasoning. During the interview, we will discuss your implementation choices, trade-offs and decision-making process, so it is important that you fully understand and can explain every part of your solution.