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