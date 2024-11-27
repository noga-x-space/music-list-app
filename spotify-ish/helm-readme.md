1. apply secrets:
```powershell
kubectl apply -f secret.yaml
```
this makes sure there's the mongo-credential secret



to install the helm package-

```powershell

kubectl get secret mongo-credentials -n default -o yaml | sed 's/namespace: default/namespace: dev/' | kubectl apply -f -


c -n dev `
> > --set secrets.mongoCredentials.username=<user-name> `
> > --set secrets.mongoCredentials.password=<password>
```

then check for the nodeport port and navigate to

- http://localhost:port
