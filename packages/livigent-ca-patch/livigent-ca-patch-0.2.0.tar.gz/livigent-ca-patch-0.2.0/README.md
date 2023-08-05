# livigent-ca-patch  

PyPi: [Link](https://pypi.org/project/livigent-ca-patch/)  
Github: [Link](https://github.com/dickermoshe/livigent-ca-patch/)  

  

### Issue:


```
requests.exceptions.SSLError: HTTPSConnectionPool(host='google.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:992)')))

OR

requests.exceptions.SSLError: HTTPSConnectionPool(host='google.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: CA certificate key too weak (_ssl.c:992)')))
```

### Solution:  

```
pip install livigent_ca_patch --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org 
```

### Usage:

```
>>> import livigent_ca_patch
>>> import requests
>>> requests.get('https://google.com')
<Response [200]>
```

