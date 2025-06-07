import hashlib
import os

def sha3_256_expand_from_binary_string(bin_str: str) -> list:

    # Zamiana ciągu binarnego na bajty
    byte_array = bytearray()
    for i in range(0, len(bin_str), 8):
        byte = int(bin_str[i:i+8], 2)
        byte_array.append(byte)

    # Hashowanie i rozszerzanie (jak w oryginalnej funkcji)
    hashed = bytearray()
    block_size = 32  # 256 bits = 32 bytes

    for i in range(0, len(byte_array), block_size):
        block = byte_array[i:i + block_size]
        h = hashlib.sha3_256(block).digest()
        hashed.extend(h)

    # Zwróć wynik jako lista intów 0–255
    return list(hashed)

# Folder z wejściowymi plikami
input_folder = "wyniki"
# Folder na wyjściowe pliki binarne jako tekst
output_folder = "wyniki_sha"
os.makedirs(output_folder, exist_ok=True)

# Przetwarzaj każdy plik .txt
for filename in sorted(os.listdir(input_folder)):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        
        # Wczytaj dane jako liczby całkowite z zakresu 0-255
        with open(input_path, "r") as f:
            content = f.read()
            numbers = list(map(int, content.strip().split()))

        # Zamień liczby na 8-bitowe ciągi binarne i sklej
        binary_string = ''.join(f"{n:08b}" for n in numbers)

        # Oblicz hash i rozszerz
        hashed_output = sha3_256_expand_from_binary_string(binary_string)

        # Zapisz wynik do nowego pliku .txt
        output_path = os.path.join(output_folder, f"sha3_{filename}")
        with open(output_path, "w") as f:
            f.write(' '.join(map(str, hashed_output)))

        print(f"[INFO] Zapisano: {output_path}")
