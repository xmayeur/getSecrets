# getSecrets package

getSecrets is a simple package that reads from the given engine ('secret' by default) of a Hashicorp vault

usage:

```
from getSecrets import *

data = get_secret(<id>, [<secret>])

usr_pwd = get_user_pwd(<id>, <new k_v_dict> , [<secret>])

list = list_secret([<secret>]

```

Vault parameters are stored in a config file ~/.config/.vault/.vault.yml

```
vault:
  token: "<access token>"
  vault_addr: "https://vault:8200"
  certs: "<path>/bundle.pem"
```