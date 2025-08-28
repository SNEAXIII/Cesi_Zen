#!/bin/bash

NAMESPACE="cesi-zen"

echo "🔄 Suppression des anciens Secrets..."
kubectl delete configmap db-env -n $NAMESPACE --ignore-not-found
kubectl delete configmap api-env -n $NAMESPACE --ignore-not-found
kubectl delete configmap front-env -n $NAMESPACE --ignore-not-found
kubectl delete secret db-env -n $NAMESPACE --ignore-not-found
kubectl delete secret api-env -n $NAMESPACE --ignore-not-found
kubectl delete secret front-env -n $NAMESPACE --ignore-not-found

echo "✅ Création du Secret db-env à partir de db.env"
kubectl create secret generic db-env \
  --from-env-file=db.env \
  -n $NAMESPACE

echo "✅ Création du Secret api-env à partir de api.env"
kubectl create secret generic api-env \
  --from-env-file=api.env \
  -n $NAMESPACE

echo "✅ Création du Secret front-env à partir de front.env"
kubectl create secret generic front-env \
  --from-env-file=front.env \
  -n $NAMESPACE

echo "🚀 Tous les Secrets sont recréés dans le namespace $NAMESPACE !"
kubectl get secrets -n $NAMESPACE
