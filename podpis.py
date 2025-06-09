import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
import os

from preprocessing_algorithm import preprocessing_algorithm
from postprocessing_sha3 import postprocessing_algorithm

# -------------------------------
# Parametry
RAMKA_POCZ = 50
RAMKA_KON = 80
BIT_COUNT = 2048
message = "Jan Kowalski".encode("utf-8")
# -------------------------------

def read_txt(path):
    with open(path, "r") as f:
        return list(map(int, f.read().strip().split()))

def get_random_bits_from_frames(n_bits, frame_start, frame_end):
    bitstream = ""

    for i in range(frame_start, frame_end, 2):
        Y_a = read_txt(f"dane_YCbCr/frame_{i:04d}_Y.txt")
        Y_b = read_txt(f"dane_YCbCr/frame_{i+1:04d}_Y.txt")
        Cb_A = read_txt(f"dane_YCbCr/frame_{i:04d}_Cb.txt")
        Cb_B = read_txt(f"dane_YCbCr/frame_{i+1:04d}_Cb.txt")
        Cr_A = read_txt(f"dane_YCbCr/frame_{i:04d}_Cr.txt")
        Cr_B = read_txt(f"dane_YCbCr/frame_{i+1:04d}_Cr.txt")

        Z = preprocessing_algorithm(Y_a, Y_b, Cb_A, Cb_B, Cr_A, Cr_B)
        bits = postprocessing_algorithm(Z)
        bitstream += ''.join(bits)

        if len(bitstream) >= n_bits:
            return bitstream[:n_bits]

    raise ValueError("Za mało danych w zadanym zakresie ramek.")

# Wygeneruj losowy strumień bitów
bitstream = get_random_bits_from_frames(BIT_COUNT, RAMKA_POCZ, RAMKA_KON)

# Zamiana na bajty
trng_data = bytes(int(bitstream[i:i+8], 2) for i in range(0, len(bitstream), 8))

# Utwórz deterministyczny klucz prywatny z SHA-256
digest = hashlib.sha256(trng_data).digest()
secp256r1_order = int("FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16)
private_int = int.from_bytes(digest, "big") % secp256r1_order
private_key = ec.derive_private_key(private_int, ec.SECP256R1())
public_key = private_key.public_key()

# Zapis kluczy i podpisu
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
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
with open(os.path.join(output_folder, "signature.bin"), "wb") as f:
    f.write(signature)

# Weryfikacja poprawności
print("Sprawdzenie podpisu")
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("Oryginalna wiadomość: podpis poprawny.")
except InvalidSignature:
    print("Oryginalna wiadomość: podpis niepoprawny!")

# Weryfikacja zmienionej wiadomości
tampered_message = "Jan KowalskI".encode("utf-8")
try:
    public_key.verify(signature, tampered_message, ec.ECDSA(hashes.SHA256()))
    print("Zmieniona wiadomość: podpis nadal działa.")
except InvalidSignature:
    print("Zmieniona wiadomość: podpis niepoprawny.")

# Weryfikacja podpisu z nieodpowiednim kluczem
digest2 = hashlib.sha256(trng_data[::-1]).digest()  
private_int2 = int.from_bytes(digest2, "big") % secp256r1_order
other_private_key = ec.derive_private_key(private_int2, ec.SECP256R1())
other_public_key = other_private_key.public_key()

try:
    other_public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("Inny klucz: podpis poprawny.")
except InvalidSignature:
    print("Inny klucz: podpis niepoprawny.")