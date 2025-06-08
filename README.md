# Podpis cyfrowy
Repozytorium dotyczy implementacji podpisu cyfrowego na podstawie **TRNG**. Projekt tworzony jest w ramach przedmiotu "Bezpieczeństwo Systemów Teleinformatycznych".

## Wytwarzanie liczb prawdziwie losowych

1. **Próbkowanie**
  - Wykonywane zdjęcia w trybie seryjnym.
  - Zapisy w formacie **YCbCr 4:2:0** (lub JPEG, jeśli niedostępne).

2. **Przetwarzanie wstępne**
  - XOR między próbkami luma/chroma z dwóch zdjęć.
  - Dane 8-bitowe trafiają do tablicy `Z`: `(Y, Cb, Y, Cr, ...)`.

3. **Przetwarzanie końcowe**
  - Mapowanie do 32-bit signed int (big-endian),
  - Normalizacja do `<0;1>` i zapis jako 64-bit `float`.

## Chaotyczna mapa logiczna (CCML);

- Nowy stan `xₜ₊₁` zależy od trzech poprzednich: `xᵢ₋₁`, `xᵢ`, `xᵢ₊₁`.  
- Iteracje: `floor(L / 2)`.

![Image](https://github.com/user-attachments/assets/960e5db4-1887-42cb-8f08-ba381c031ec4)

## Uruchamianie

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/vanshor/PodpisCyfrowy
```

### 2. Instalacja zależności

```bash
pip install opencv-python numpy cryptography
```

### 3. Generowanie danych TRNG

```bash
cd PodpisCyfrowy
python pobieranie_danych.py
python preprocessing_algorithm.py
python sha3-256.py
python postprocessing_sha3.py
```

### 4. Podpisanie wiadomości

```bash
python podpis.py
```

## Wykonano przez
- Vansh Dixit 156136
