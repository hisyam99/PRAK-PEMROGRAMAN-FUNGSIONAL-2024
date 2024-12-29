from PIL import Image, ImageEnhance, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import os

def load_gambar(folder_path):
    gambar_array = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            image = image.resize((300, 300)) 
            gambar_array.append(np.array(image))
    return gambar_array

def edit_gambar(image_array):
    image = Image.fromarray(image_array)
    enhancer = ImageEnhance.Brightness(image)  
    image = enhancer.enhance(1.3)  
    image = ImageOps.expand(image, border=10, fill='black')  
    enhancer = ImageEnhance.Sharpness(image)  
    image = enhancer.enhance(1.5)  
    return np.array(image)

def watermark_gambar(image_array, watermark_path):
    image = Image.fromarray(image_array)
    watermark = Image.open(watermark_path).convert('RGBA')
    watermark = watermark.resize((50, 50))  # Ukuran watermark dikecilkan
    pos = (image.size[0] - watermark.size[0] - 10, image.size[1] - watermark.size[1] - 10)  # Posisi watermark di ujung kanan gambar
    image = image.convert('RGBA')
    image.paste(watermark, pos, watermark)
    
    
    
    return np.array(image)

def grayscale_gambar(image_array):
    image = Image.fromarray(image_array)
    image = image.convert('L')  
    return np.array(image)

def show_perbandingan(image_array, edited_image_array):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(image_array)
    axs[0].set_title('Gambar Asli')
    axs[1].imshow(edited_image_array)
    axs[1].set_title('Gambar Hasil Edit')
    plt.show()

def main():
    folder_path = 'gambar_produk'
    watermark_path = 'watermark.png'
    edited_folder_path = 'edited_gambar_produk'
    if not os.path.exists(edited_folder_path):
        os.makedirs(edited_folder_path)
    gambar_array = load_gambar(folder_path)
    edited_array = []
    for image_array in gambar_array:
        edited_image_array = edit_gambar(image_array)
        edited_image_array = watermark_gambar(edited_image_array, watermark_path)
        if input("Apakah produk ini habis? (y/n): ") == 'y':
            edited_image_array = grayscale_gambar(edited_image_array)
        if edited_image_array.ndim == 2:
            edited_image_array = edited_image_array.reshape((edited_image_array.shape[0], edited_image_array.shape[1], 1))
            edited_image_array = np.repeat(edited_image_array, 3, axis=2)
        edited_image = Image.fromarray(edited_image_array.astype(np.uint8))
        edited_image = edited_image.convert('RGB')
        edited_image_path = os.path.join(edited_folder_path, f'edited_{len(edited_array)}.png')
        edited_image.save(edited_image_path)
        edited_array.append(edited_image_array)
    for i, image_array in enumerate(gambar_array):
        edited_image_array = edited_array[i]
        show_perbandingan(image_array, edited_image_array)

if __name__ == '__main__':
    main()