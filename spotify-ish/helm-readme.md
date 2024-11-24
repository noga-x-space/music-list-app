to install the helm package-

```powershell
helm install spotify-ish ./spotify-ish -n dev `
> > --set secrets.mongoCredentials.username=<user-name> `
> > --set secrets.mongoCredentials.password=<password>
```
then check for the nodeport port and navigate to 
- http://localhost:port