# Deployment Steps

## Important configuration settings
* DNS: The A record for gogs.silicon-ctf.party is configured in GoDaddy
* In `ingress.yaml`, `nginx.ingress.kubernetes.io/whitelist-source-range` is configured to only allow connections from Intel proxies

## Push image to container registry
1. `docker pull splunk/splunk`
2. `docker tag splunk/splunk registry/splunk/splunk`
3. `docker login registry`
    Creds for the registry are found in the Azure Portal
4. `docker push registry/splunk/splunk`

## Deploy to K8S
1. Copy secret.yaml.example to secret.yaml and update the password to a base64 encoded string (at least 8 characters)
2. Create namespace `kubectl apply -f namespace.yaml`
3. Create persistant volume claim `kubectl apply -f pvc.yaml`
4. Create service `kubectl apply -f service.yaml`
5. Create ingress `kubectl apply -f ingress.yaml`
6. Create secret `kubectl apply -f secret.yaml`
7. Create deployment `kubectl apply -f deployment.yaml`