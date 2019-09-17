## Architecture

## Setup

```
gcloud beta container clusters create rundemo \
  --addons=HorizontalPodAutoscaling,HttpLoadBalancing,Istio,CloudRun \
  --machine-type=n1-standard-4 \
  --cluster-version=latest \
  --enable-stackdriver-kubernetes \
  --enable-ip-alias \
  --scopes cloud-platform
```

`gcloud container clusters get-credentials rundemo`


`gcloud config set run/platform gke`
`gcloud config set run/cluster rundemo`
`gcloud config set run/cluster_location us-central1-f`

`kubectl get svc -n istio-system istio-ingressgateway -o jsonpath={.status.loadBalancer.ingress..ip}`

```
kubectl patch configmap config-domain --namespace knative-serving --patch \
  '{"data": {"example.com": null, "[INGRESS].xip.io": ""}}'
```

## Building

```
for d in account-balance bank-holdings compute-transaction transaction-generator; \
  do gcloud builds submit $d/ \
    --tag gcr.io/[PROJECT]/$d:0.1 \
    --project [PROJECT] \
    --async; done
```

## Deploying

### Database

`kubectl apply -f database/mongodb.yaml`

### Apps

```
for a in account-balance bank-holdings; \
  do gcloud beta run deploy $a \
    --image gcr.io/[PROJECT]/$a:0.1 \
    --connectivity external; done
```

```
gcloud beta run deploy compute-transaction \
  --image gcr.io/[PROJECT]/compute-transaction:0.1 \
  --connectivity internal
```

```
gcloud beta run deploy transaction-generator \
  --image gcr.io/[PROJECT]/transaction-generator:0.1 \
  --set-env-vars API=compute-transaction.default.[INGRESS].xip.io, \
  --connectivity external
```

## Usage

Open `http://transaction-generator.default.[INGRESS].xip.io` and generate some transactions. Then, go to `http://bank-holdings.default.[INGRESS].xip.io` and check the bank's balance. Finally, go to `http://account-balance.default.[INGRESS].xip.io` and see how much money you have, based on the fractions of a penny left over from each transaction.

## Cleanup

`gcloud container clusters delete rundemo`


