import time
import math

# 1. Decorator untuk menghitung waktu eksekusi
def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

# 2. Menerima input dan memetakannya ke (x, y)
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

# 3. Higher-Order Function untuk transformasi
def create_transformation(func):
    """Higher-Order Function yang menghasilkan fungsi transformasi."""
    def transformation(*args):
        return func(*args)
    return transformation

# 4. Translasi (Closure + Lambda Expression)
@execution_time
def translation(tx, ty):
    return lambda points: [(x + tx, y + ty) for x, y in points]

# 5. Rotasi (Closure + Lambda Expression)
@execution_time
def rotation(angle_degrees):
    angle_radians = math.radians(angle_degrees)
    return lambda points: [
        (
            x * math.cos(angle_radians) - y * math.sin(angle_radians),
            x * math.sin(angle_radians) + y * math.cos(angle_radians),
        )
        for x, y in points
    ]

# 6. Dilatasi (Closure + Lambda Expression)
@execution_time
def dilation(scale_factor):
    return lambda points: [(x * scale_factor, y * scale_factor) for x, y in points]

# 7. Melakukan transformasi berurutan (Higher-Order Function + First-Class Function)
@execution_time
def apply_transformations(points, transformations):
    for i, transform in enumerate(transformations):
        points = transform(points)  # Fungsi transformasi diterapkan
        print(f"Hasil setelah transformasi {i + 1}: {points}")
    return points

# Main Program
if __name__ == "__main__":
    # Input dari pengguna
    user_input = input("Masukkan angka yang dipisahkan dengan koma (contoh: 1,2,3,4): ")
    
    # Memetakan input menjadi pasangan (x, y)
    points = map_to_points(user_input)
    if isinstance(points, str):  # Handle jika terjadi error
        print("Error:", points)
    else:
        print("Original points:", points)

        # Meminta input transformasi dari pengguna
        tx = int(input("Masukkan nilai translasi tx: "))
        ty = int(input("Masukkan nilai translasi ty: "))
        angle = float(input("Masukkan sudut rotasi (dalam derajat): "))
        scale_factor = float(input("Masukkan faktor skala untuk dilatasi: "))

        # Membuat transformasi menggunakan Higher-Order Function
        translate = create_transformation(translation(tx, ty))
        rotate = create_transformation(rotation(angle))
        dilate = create_transformation(dilation(scale_factor))

        transformations = [translate, rotate, dilate]
        final_points = apply_transformations(points, transformations)
        
        print("Final transformed points:", final_points)
