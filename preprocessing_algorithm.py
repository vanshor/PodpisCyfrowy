def preprocessing_algorithm(Y_a, Y_b, Cb_A, Cb_B, Cr_A, Cr_B): #funkcja dziala poprawnie dla danych podanych dziesietnie i binarnie
    luma_final = []
    Cb_final = []
    Cr_final = []
    Z = []
    dlugosc_lumy = len(Y_a)
    dlugosc_chromy = len(Cb_A)

    for i in range(dlugosc_lumy):
        luma_final.append(Y_a[i] ^ Y_b[dlugosc_lumy-i-1])

    for i in range(dlugosc_chromy):
        Cb_final.append(Cb_A[i] ^ Cb_B[dlugosc_chromy-i-1])
        Cr_final.append(Cr_A[i] ^ Cr_B[dlugosc_chromy-i-1])

    Cb = True
    for i in range(dlugosc_lumy + 2*dlugosc_chromy): #16y 4cr 4cb
        if i < dlugosc_lumy: #do momentu gdy musimy jeszcze dodawac chromy
            if i % 2 == 0:
                Z.append(luma_final[i//2])
            else:
                if Cb:
                    Z.append(Cb_final[(i-1)//4])
                    Cb = False
                else:
                    Z.append(Cr_final[(i-3)//4])
                    Cb = True
        else: #dodajemy juz tylko pozostale probki lumy
            temp = i // 2
            Z.append(luma_final[temp])
            temp+=1

    return Z


def read_txt_file(f):
    return list(map(int, f.read().strip().split()))

def zapisz(): #zapisywanie wartosci tablicy "Z" do plikow txt
    ilosc_ramek = 146
    for i in range(24, ilosc_ramek, 2): #odrzucamy 24 pierwsze ramki, tak zalecono
        prefix = f"dane_YCbCr/frame_{i:04d}"
        prefix2 = f"dane_YCbCr/frame_{(i + 1):04d}"
        with open(f"{prefix}_Y.txt") as f1, \
             open(f"{prefix2}_Y.txt") as f2, \
             open(f"{prefix}_Cb.txt") as f3, \
             open(f"{prefix2}_Cb.txt") as f4, \
             open(f"{prefix}_Cr.txt") as f5, \
             open(f"{prefix2}_Cr.txt") as f6:

            Y_a = read_txt_file(f1)
            Y_b = read_txt_file(f2)
            Cb_A = read_txt_file(f3)
            Cb_B = read_txt_file(f4)
            Cr_A = read_txt_file(f5)
            Cr_B = read_txt_file(f6)

            result = preprocessing_algorithm(Y_a, Y_b, Cb_A, Cb_B, Cr_A, Cr_B)

            # Zapis wyniku do pliku
            output_filename = f"wyniki/tablica_Z_z_ramek{i:04d}_i_{(i+1):04d}.txt"
            with open(output_filename, 'w') as out_f:
                out_f.write(' '.join(map(str, result)))

if __name__ == "__main__":
    zapisz()
    # mamy juz zapisane wartosci tablicy Z ktore beda wejsciem do post processingu
    # do zrobienia post processing
    with open("dane_YCbCr/frame_0080_Y.txt") as f1:
        Y_a = read_txt_file(f1)
        for i in range(5):
            print(Y_a[i])

