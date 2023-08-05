# This patch allows the use of 1024 bit keys for the CA certificates.
import ssl 
ctx = ssl.create_default_context()
ctx.set_ciphers('DEFAULT@SECLEVEL=1')
ssl.create_default_context = lambda: ctx

