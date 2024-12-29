import time
import math

# Dekorator untuk menghitung waktu eksekusi
def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

# 1. Menerima input dan memetakannya ke (x, y)
@execution_time
def map_to_points(input_str):
    try:
        numbers = list(map(int, input_str.split(',')))
        if len(numbers) % 2 != 0:
            raise ValueError("Jumlah angka harus genap untuk membentuk pasangan (x, y).")
        points = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]
        return points
    except ValueError as e:
        return str(e)

# 2. Membuat fungsi transformasi
# Translasi
@execution_time
def translation(tx, ty):
    def apply_translation(points):
        return [(x + tx, y + ty) for x, y in points]
    return apply_translation

# Rotasi
@execution_time
def rotation(angle_degrees):
    angle_radians = math.radians(angle_degrees)
    def apply_rotation(points):
        return [(
            x * math.cos(angle_radians) - y * math.sin(angle_radians),
            x * math.sin(angle_radians) + y * math.cos(angle_radians)
        ) for x, y in points]
    return apply_rotation

# Dilatasi
@execution_time
def dilation(scale_factor):
    def apply_dilation(points):
        return [(x * scale_factor, y * scale_factor) for x, y in points]
    return apply_dilation

# 3. Melakukan transformasi berurutan
@execution_time
def apply_transformations(points, transformations):
    for i, transform in enumerate(transformations):
        points = transform(points)
        print(f"Hasil setelah transformasi {i + 1}: {points}")
    return points

# Main Program
if __name__ == "__main__":
    # Meminta input dari user
    user_input = input("Masukkan angka yang dipisahkan dengan koma (contoh: 1,2,3,4): ")
    
    # Proses
    points = map_to_points(user_input)
    if isinstance(points, str):  # Handle error message dari map_to_points
        print("Error:", points)
    else:
        print("Original points:", points)

        # Meminta input transformasi dari pengguna
        tx = int(input("Masukkan nilai translasi tx: "))
        ty = int(input("Masukkan nilai translasi ty: "))
        angle = float(input("Masukkan sudut rotasi (dalam derajat): "))
        scale_factor = float(input("Masukkan faktor skala untuk dilatasi: "))

        # Buat fungsi transformasi
        translate = translation(tx, ty)
        rotate = rotation(angle)
        dilate = dilation(scale_factor)

        # Terapkan transformasi secara bertahap
        transformations = [translate, rotate, dilate]
        final_points = apply_transformations(points, transformations)
        
        # Cetak hasil akhir
        print("Final transformed points:", final_points)
