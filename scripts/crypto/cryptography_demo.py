from cryptography.fernet import Fernet
import sys

msg = sys.argv[1].encode("utf-8")
key = Fernet.generate_key()
print("Key: " + key.decode("ascii"))
f = Fernet(key)
token = f.encrypt(msg)
print("Encrypted: " + token.decode("utf-8"))
msg = f.decrypt(token)
print("Decrypted: " + msg.decode("utf-8"))
