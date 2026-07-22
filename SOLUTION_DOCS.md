# Documenting in the meantime of solving the assessment

I’m iterating on the assessment and keeping notes as I go.

## Iteration 1

### Python

Built a small Python service in `app/app.py` with the required endpoints:
- `GET /health`
- `GET /version`
- `GET /env`
- `POST /config`
- `GET /config/{name}`
- `DELETE /config/{name}`

Added a simple test script in `app/test_requests.sh` and a minimal `app/Dockerfile`.

### Helm / Terraform

Found chart mismatches that block deployment:
- service selector label mismatch (`myapp` vs `myapps`)
- ingress backend points to the wrong service (`homeworks` instead of `myapp`)
- container port mismatch (`5000` vs `8080`)

Was able to init and install the helm chart with the first, basic image version. 
Solved the image passing problem through the docker deamon to the k3s with `docker save` and `k3s ctr images import` commands. Didn't want to take time with external container registry.

## End of Iteration 1.

## Iteration 2.

### Gitlab-ci-local

I've tried to run all the jobs with Gitlab-Ci-Local, to make sure everything is working as expected, but I was always running into different network or permission errors. I've started to check whats the issue, so I can resolve that easily, but turned into a really deep rabbit hole, so I've decided to just let it go due to the small timebox. I don't usually like leaving issues unresolved, but it felt like the right trade-off for this assessment.

Commited all the gitlab-ci-local related configs, maybe anyone else can try it out.

More information: https://github.com/firecow/gitlab-ci-local

Examples: https://github.com/firecow/gitlab-ci-local/tree/master/examples

#### Disclaimer: I probably spent an extra 1–1.5 hours trying to get GitLab-CI-Local working. If that time is included, the total effort exceeded the suggested 3 hours. Personally, I don't think it should count, as it was related to my local development environment and related to my own decision rather than the assessment itself, but I wanted to mention it for transparency.

### Terraform issues/small improvements
- Multiple issues on the set block in main.tf:
    - Missing value in `value` of `image.tag`
    - Missing `=` character after the `set` keyword and before the entities
    - Multiple set blocks are not supported, changed as one set block, and changed all of them to the variable mappings which were defined in the variables.tf
- Missing `=` character inside of providers.tf in Helm, within Kubernetes config part
- The prepared config_path for the kubernetes wasn't the same like my k3s installation created by default, changed to my working value.
- The `chart      = "../helm/homework"` wasn't the proper value with the prepared helm chart folder structure, changed to `chart      = "../helm"`
- Created a `tfvars/prod_terraform.tfvars` for the "PROD" variables to prevent hardcoded values or manual declaration. (These values are overwriting the Helm chart values, didn't change on Helm value to be able to run with local helm command with already prepared imagge name)
- Also changed the hardcoded "production" namespace to the variable which was already created in the variables.tf.


### Gitlab CI

- Added quite robust Gitlab CI jobs and configs (maybe too robust for the assessment)
- Created a small Docker build job which just builds and pushed the image to the registry I was running on the AKS Cluster. (Left some attributes regarding the Gitlab-ci-local, these might end up in erros in real Gitlab pipelines)
- Created a `terraform_setup` anchor with all the parts which every terraform might use.
- I've changed the prepared "deploy" job to a `terraform plan` and dedicated `terraform apply` job
    - The plan job uses the tfvars within the job command.
    - The plan saves the tfplan and passes the artifacts to the apply job
- Added additional `terraform_destroy_plan` and `terraform_destroy_apply` jobs which only appears on the real pipeline if the env variable of `CONFIRM_TO_DESTROY` equals to `true`. Just to try to ease my work on the testing. And also might be useful in real-world examples.
- Added local "job" `variable-set-job-for-local-test` which enables to copy and paste the whole job with all the commands to set the variables which would be set by the pipeline itself on a real one.

## End of Iteration 2.

## Iteration 3.

### Terraform

- Realized some warnings regarding deprecated resource name
    - Replaced `kubernetes_namespace` -> `kubernetes_namespace_v1` on both places

### Gitlab CI

- added "assessment" prefix for preparing to deploy multiple stacks from one repo, if needed, to prevent naming conflicts
- moved the `terraform_setup` anchor to avoid missing this setup running on local environment
- added missing `CI_PIPELINE_ID` variable example
- renamed the `build` job -> `docker-build-and-push`
- removed a `dependencies` block -> as far as I know the needs completely does the same in our context
- added the `terraform_apply` as the optional needs of destroy (only destroy after deploying, but preparing also for destroyingg it in a different pipeline)
- added a `destroy` word for the destroy job to prevent mixed TF Plan files

### README.md

- Filled in the remaining parts of the Readme

### USER_GUIDE.md

- Created a separate USER_GUIDE with a short "howto" to install and use the stack I've prepared