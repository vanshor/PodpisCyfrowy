import struct

def logistic_map(x, r, c):
    if x == 0.0:
        x = r / 4.0
    r += 0.001 * x + c
    if r > 4.0:
        r = 3.9 + 0.0025 * r
    for _ in range(50):
        x = r * x * (1 - x)
    return x, r

def postprocessing_algorithm(Z, L=6, epsilon=0.5, c=0.002):
    #result = {i: 0 for i in range(256)}
    O = []
    j = 0
    min_z = min(Z)
    max_z = max(Z)
    
    if min_z == max_z:
        raise ValueError("Z has zero dynamic range.")

    while j < len(Z):
        # Krok 1: normalizacja
        x = []
        for i in range(L):
            idx = (j + i) % len(Z)
            x_norm = (Z[idx] - min_z) / (max_z - min_z)
            x.append(float(x_norm))

        r = [3.9 for _ in range(L)]
        num_iterations = L // 2

        for _ in range(num_iterations):
            f_x = [0.0] * L
            new_x = [0.0] * L
            new_r = [0.0] * L

            # Logistic map i perturbacja r
            for i in range(L):
                xi, ri = logistic_map(x[i], r[i], c)
                f_x[i] = xi
                new_r[i] = ri

            # CCML - sprzężenie
            for i in range(L):
                next_i = (i + 1) % L
                prev_i = (i - 1 + L) % L
                new_x[i] = epsilon * f_x[i] + (1 - epsilon) / 2 * (f_x[next_i] + f_x[prev_i])

            x = new_x
            r = new_r

        # Krok 4: kompresja float64 -> 32 bity
        for xi in x:
            bytes_val = struct.pack('>d', xi)  # float64 big-endian
            msb32 = int.from_bytes(bytes_val[:4], 'big')
            lsb32 = int.from_bytes(bytes_val[4:], 'big')
            xor_val = msb32 ^ lsb32
            liczba = f"{xor_val:032b}"
            O.append(liczba)

            ## Liczba 32-bitowa -> 4 bajty
            #result[int(liczba[0:8], 2)] += 1
            #result[int(liczba[8:16], 2)] += 1
            #result[int(liczba[16:24], 2)] += 1
            #result[int(liczba[24:32], 2)] += 1

        j += L

    #print(result)
    #print(O)
    return O

# Wczytaj dane
file_path = "wyniki/tablica_Z_z_ramek0050_i_0051.txt"

with open(file_path, 'r') as file:
    Z = list(map(int, file.read().strip().split()))
    wynik = postprocessing_algorithm(Z)


# Sklej wszystko w jeden długi string
bitstream = ''.join(wynik)


# Podziel na bajty i zamień na inty
byte_values = [
    int(bitstream[i:i+8], 2)
    for i in range(0, len(bitstream), 8)
]

# Zapisz do pliku binarnego
with open("wyjscie_bin.bin", "wb") as f:
    f.write(bytes(byte_values))

#with open("wyjscie_bin.txt", "w") as f:
#    f.write(bitstream)

#tutaj jest glowny postprocessing