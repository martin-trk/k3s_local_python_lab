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

