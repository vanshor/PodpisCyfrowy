import hashlib
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from postprocessing_sha3 import postprocessing_algorithm

# Wczytaj dane wejściowe do postprocessingu z SHA3
file_path = "wyniki_sha/sha3_tablica_Z_z_ramek0050_i_0051.txt"
with open(file_path, "r") as f:
    Z = list(map(int, f.read().strip().split()))

# Uruchom postprocessing
bit_blocks = postprocessing_algorithm(Z)
bitstream = ''.join(bit_blocks)

# Zamień bitstream na bajty w pamięci 
trng_data = bytes(
    int(bitstream[i:i+8], 2)
    for i in range(0, len(bitstream), 8)
)

# Użyj TRNG do deterministycznego klucza
digest = hashlib.sha256(trng_data).digest()
secp256r1_order = int("FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16)
private_int = int.from_bytes(digest, "big") % secp256r1_order
private_key = ec.derive_private_key(private_int, ec.SECP256R1())
public_key = private_key.public_key()

# Zapisz klucze i podpis do katalogu
output_folder = "podpis_output"
os.makedirs(output_folder, exist_ok=True)

with open(os.path.join(output_folder, "ecdsa_private_key.pem"), "wb") as f:
    f.write(private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    ))

with open(os.path.join(output_folder, "ecdsa_public_key.pem"), "wb") as f:
    f.write(public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# Podpisanie wiadomości
message = "Jan Kowalski".encode("utf-8")
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
with open(os.path.join(output_folder, "signature.bin"), "wb") as f:
    f.write(signature)

print("Sprawdzenie podpisu")
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("Oryginalna wiadomość: podpis poprawny.")
except InvalidSignature:
    print("Oryginalna wiadomość: podpis niepoprawny!")

# Podmiana wiadomości 
tampered_message = "Jan KowalskI".encode("utf-8")
try:
    public_key.verify(signature, tampered_message, ec.ECDSA(hashes.SHA256()))
    print("Zmieniona wiadomość: podpis nadal działa")
except InvalidSignature:
    print("Zmieniona wiadomość: podpis niepoprawny.")
