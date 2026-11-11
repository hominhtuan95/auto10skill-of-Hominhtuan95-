import base64
import json
import sys
from pathlib import Path
from cryptography.hazmat.primitives import serialization

APP_NAME = 'Autoskill Hominhtuan95'
if len(sys.argv) != 2:
    raise SystemExit('Usage: python issue_license.py HWID')
hwid = sys.argv[1].strip().upper()
if len(hwid) != 32 or any(c not in '0123456789ABCDEF' for c in hwid):
    raise SystemExit('HWID must contain 32 hexadecimal characters')
private = serialization.load_pem_private_key((Path(__file__).parent / 'PRIVATE_LICENSE_KEY.pem').read_bytes(), password=None)
payload = json.dumps({'app': APP_NAME, 'hwid': hwid, 'version': 1}, sort_keys=True, separators=(',', ':')).encode()
signature = private.sign(payload)
def b64(b): return base64.urlsafe_b64encode(b).decode().rstrip('=')
print('License key:')
print(b64(payload) + '.' + b64(signature))
