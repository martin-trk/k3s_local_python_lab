## Code Review
Hey!

Nice work getting this far, the structure and the plan looks good, I've just realized some syntax errors and missalignments in Terraform code and Helm labels.
I would suggest you to try to run `terraform init`/`terraform validate`/`terraform plan` (if the environment accepts that, or it is possible).
We are also planning to implement these kind of feedback loops into the feature/ branch pipelines, or creating a pre-commit hook for these.

A few pointers on where to look:

1. The **first issue** I was running into when trying to deploy it, was the **missing value on some of the set blocks**. The name was there, but the value was empty, that was the first blocker of the terraform commands, please check that. And also, I think the Terraform does not support multiple `set` blocks, even if you add the value there. It worth to check
[Helm Provider's offical docs](https://registry.terraform.io/providers/-/helm/latest/docs).
2. If I can see it right, the Helm chart **folder structure** is not prepared in the **same way** like you declared it in `main.tf`.
3. I can also see **some missalignments on the Helm chart labels**. These labels are important, because thats how the Kubernetes connects its resources together.
For example, the "template" part of the `deployment.yml` expects to have the same `labels: app: myapp` on the `template:` level (which is the template of pods it is creating), as the parent block's (deployment's) `selector: matchLabels: app: myapp`. Until that point, everything you did is good. The problem is with the Service's label selector. It will try to search for `app: myapps` instead of `app: myapp`. Please correct on one of the ends which you like to keep. The same applies to Ingress, the service label mismatches. I won't spoiler it down, please take a look at it.
Docs: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
4. There is also a mismatch on the **Ports section** of the network flow. The network is flowing through the following way: 
    .... -> Ingress will try to connect to the service described in `ingress.yaml`, on port 80 -> Service (myapp) which serves port 80 -> The service maps the port 80 (Service's port) to the pod's `targetPort` 8080 (alogn with the help of the selector) -> It will try to connect to the pod on the `targetPort`, which is 8080 (`service.yaml`)-> The deployment also describes a port on the container/pod level, which we are exposing to the service (`deployment.yaml`)

    Docs: https://kubernetes.io/docs/tutorials/services/connect-applications-service/
5. I would recommend you to try to avoid hardcoded values. Please replace the hardcoded `production` in `main.tf` with the proper variable, since you've already declared it.

And once again, in general, I would recommend you to run `terraform init`/`terraform validate`/`terraform plan` along with trying the Helm charts on your local machine, if there is any configured to troubleshoot and test the changes, along with trying `helm lint` and `helm template`. The label mismatch won't be discovered by the lint and template, but it can check other syntax error if that occurs.