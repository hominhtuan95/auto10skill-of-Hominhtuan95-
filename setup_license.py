from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

folder = Path(__file__).resolve().parent
private_path = folder / 'PRIVATE_LICENSE_KEY.pem'
app_path = folder / 'Autoskill_Hominhtuan95.py'
if private_path.exists():
    raise SystemExit('PRIVATE_LICENSE_KEY.pem already exists. Refusing to overwrite it.')
if not app_path.exists():
    raise SystemExit('Missing Autoskill_Hominhtuan95.py')
text = app_path.read_text(encoding='utf-8')
if "REPLACE_WITH_PUBLIC_KEY" not in text:
    raise SystemExit('Public key already configured; refusing to replace it.')
key = Ed25519PrivateKey.generate()
public_hex = key.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
).hex()
private_path.write_bytes(key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
))
app_path.write_text(text.replace('REPLACE_WITH_PUBLIC_KEY', public_hex), encoding='utf-8')
print('Configured public key in app. Keep PRIVATE_LICENSE_KEY.pem OFF GitHub!')
