import random
import hashlib
import base64

def generate_key_secret():
    """docstring for generate_key_secret"""
    a = base64.b64encode(hashlib.sha224(str(random.getrandbits(256))).digest(),
                         random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')[0:18]
    b = base64.b64encode(hashlib.sha224(str(random.getrandbits(256))).digest(),
                         random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')

    return { 'key': a, 'secret': b }


key_secret = generate_key_secret()
print "key: %s" % key_secret['key']
print "secret: %s" % key_secret['secret']