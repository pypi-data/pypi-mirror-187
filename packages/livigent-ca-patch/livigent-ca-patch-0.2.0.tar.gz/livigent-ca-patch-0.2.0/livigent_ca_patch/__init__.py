import pip_system_certs.wrapt_requests # Wraps requests with system certificates
from . import allow_1024 # This patch allows the use of 1024 bit keys for the CA certificates.
