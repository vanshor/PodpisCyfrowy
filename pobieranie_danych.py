import cv2
import numpy as np
import os

# Ustawienia
video_path = "film_z_balkonu.mp4"  # <- zmień na ścieżkę do swojego filmu
output_dir = "dane_YCbCr"
os.makedirs(output_dir, exist_ok=True)

# Otwórz film
cap = cv2.VideoCapture(video_path)
frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Konwersja BGR -> YCrCb
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    Y_full = ycrcb[:, :, 0]
    Cr_full = ycrcb[:, :, 1]
    Cb_full = ycrcb[:, :, 2]

    # 4:2:0 subsampling: Cb i Cr co 2x2 piksele
    Cb_420 = Cb_full[::2, ::2]
    Cr_420 = Cr_full[::2, ::2]

    # Zapisz dane jako tekst
    Y_flat = Y_full.flatten()
    Cb_flat = Cb_420.flatten()
    Cr_flat = Cr_420.flatten()

    frame_id = f"{frame_number:04d}"

    with open(f"{output_dir}/frame_{frame_id}_Y.txt", "w") as f:
        f.write(' '.join(map(str, Y_flat)))

    with open(f"{output_dir}/frame_{frame_id}_Cb.txt", "w") as f:
        f.write(' '.join(map(str, Cb_flat)))

    with open(f"{output_dir}/frame_{frame_id}_Cr.txt", "w") as f:
        f.write(' '.join(map(str, Cr_flat)))

    print(f"Klatka {frame_number} zapisana.")
    frame_number += 1

cap.release()
print("Zakończono.")
