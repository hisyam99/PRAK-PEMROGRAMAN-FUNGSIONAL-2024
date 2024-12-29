import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance

def process_image(input_path, output_path):
    # Step 1: Baca gambar input menggunakan OpenCV
    img = cv2.imread(input_path)
    if img is None:
        print("Gambar tidak ditemukan!")
        return

    # Step 2: Konversi gambar ke HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Step 3: Modifikasi saturasi dan hue untuk efek langit pink
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 65)  # Tingkatkan saturasi
    h = cv2.add(h, 1)   # Geser hue sedikit ke pink

    hsv_modified = cv2.merge([h, s, v])
    img_modified = cv2.cvtColor(hsv_modified, cv2.COLOR_HSV2BGR)

    # Step 4: Tingkatkan kontras dan brightness untuk keseluruhan gambar
    alpha = 2.4  # Kontras
    beta = -10   # Brightness
    img_final = cv2.convertScaleAbs(img_modified, alpha=alpha, beta=beta)

    # Step 5: Konversi ke format Pillow untuk peningkatan saturasi lebih lanjut
    pil_img = Image.fromarray(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Color(pil_img)
    pil_img_enhanced = enhancer.en  hance(1.5)  # Tingkatkan saturasi lebih lanjut

    # Step 6: Crop gambar
    cropped_img = pil_img_enhanced.crop((0, 25, 500, 440))

    # Step 7: Resize untuk menjaga aspek rasio
    original_aspect_ratio = img.shape[1] / img.shape[0]
    new_width = cropped_img.width
    new_height = int(new_width / original_aspect_ratio)
    stretched_img = cropped_img.resize((new_width, new_height), Image.Resampling.BILINEAR)

    # Step 8: Simpan hasil akhir
    stretched_img.save(output_path)

    print("Gambar berhasil diproses dan disimpan di:", output_path)

    # Tampilkan hasil dengan matplotlib
    plt.figure(figsize=(10, 5))

    # Subplot untuk gambar sebelum diedit
    plt.subplot(1, 2, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.title("Gambar Awal")
    plt.imshow(img_rgb)
    plt.axis("off")

    # Subplot untuk gambar setelah diedit dan dicrop
    plt.subplot(1, 2, 2)
    plt.title("Gambar Kedua")
    plt.imshow(stretched_img)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# Path gambar input dan output
input_path = "images/Gedung 5 UMM-thumbnail.jpg"  # Ganti dengan path gambar awal Anda
output_path = "gambar_kedua.jpg"

# Panggil fungsi
process_image(input_path, output_path)
