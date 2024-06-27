# getSecrets package

getSecrets is a simple package that reads from the 'secret' repository of a Hashicorp vault

usage:

```
from get_secrets import get_secret

data = get_secret(<id>)
```

If the secret is a single key/value pair, data is a type tuple(key, value)
else, data is a dictionary

Vault parameters are stored in a config file ~/.config/.vault/.vault.yml

```
vault:
  token: "<access token>"
  vault_addr: "https://vault:8200"
  certs: "<path>/bundle.pem"
```