data_penjualan = [
    {"id_produk": "GN101", "nama_produk": "Kemeja", "harga": 150000, "quantity": 3, "tanggal": "2024-08-05"},
    {"id_produk": "GN102", "nama_produk": "Celana", "harga": 100000, "quantity": 4, "tanggal": "2024-08-05"},
    {"id_produk": "GN103", "nama_produk": "Topi", "harga": 50000, "quantity": 10, "tanggal": "2024-08-05"},
    {"id_produk": "GN104", "nama_produk": "Sepatu", "harga": 250000, "quantity": 2, "tanggal": "2024-08-06"},
    {"id_produk": "GN105", "nama_produk": "Tas", "harga": 300000, "quantity": 1, "tanggal": "2024-08-06"},
    {"id_produk": "GN106", "nama_produk": "Kacamata", "harga": 100000, "quantity": 5, "tanggal": "2024-08-06"},
    {"id_produk": "GN107", "nama_produk": "Sweater", "harga": 200000, "quantity": 3, "tanggal": "2024-08-07"},
    {"id_produk": "GN108", "nama_produk": "Jaket", "harga": 350000, "quantity": 1, "tanggal": "2024-08-07"},
    {"id_produk": "GN109", "nama_produk": "Kaos", "harga": 80000, "quantity": 2, "tanggal": "2024-08-07"},
    {"id_produk": "GN110", "nama_produk": "Sandal", "harga": 40000, "quantity": 7, "tanggal": "2024-08-08"},
    {"id_produk": "GN111", "nama_produk": "Jas", "harga": 500000, "quantity": 1, "tanggal": "2024-08-08"},
    {"id_produk": "GN112", "nama_produk": "Ikat Pinggang", "harga": 70000, "quantity": 4, "tanggal": "2024-08-08"}
]

# Pure function untuk menghitung pendapatan per produk
def hitung_pendapatan(data):
    return [
        {
            **produk,
            "pendapatan": produk["harga"] * produk["quantity"]
        }
        for produk in data
    ]

# Pure function untuk menghitung rata-rata penjualan di tanggal tertentu
def average_penjualan(tanggal, data):
    try:
        # Filter produk berdasarkan tanggal
        produk_di_tanggal = [produk for produk in data if produk["tanggal"] == tanggal]
        if not produk_di_tanggal:
            raise ValueError("Tidak ada penjualan pada tanggal tersebut.")
        
        # Menghitung rata-rata pendapatan
        total_pendapatan = sum(produk["pendapatan"] for produk in produk_di_tanggal)
        rata_rata = total_pendapatan / len(produk_di_tanggal)
        return f"Rata-rata penjualan pada tanggal {tanggal}: Rp{rata_rata:.2f}"
    
    except ValueError as e:
        return str(e)

# Fungsi generator untuk menghitung total penjualan per tanggal (pure function)
def total_penjualan(data):
    tanggal_unik = sorted(set(produk["tanggal"] for produk in data))
    for tanggal in tanggal_unik:
        total = sum(produk["pendapatan"] for produk in data if produk["tanggal"] == tanggal)
        yield f"Tanggal: {tanggal}, Total Penjualan: Rp{total}"

def main_menu():
    data_dengan_pendapatan = hitung_pendapatan(data_penjualan)
    total_penjualan_generator = total_penjualan(data_dengan_pendapatan)

    while True:
        print("\n--- Main Menu ---")
        print("1. Tampilkan pendapatan setiap produk")
        print("2. Hitung rata-rata penjualan berdasarkan tanggal")
        print("3. Tampilkan total penjualan per tanggal")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1/2/3/4): ")
        
        if pilihan == "1":
            for produk in data_dengan_pendapatan:
                print(f"Product ID: {produk['id_produk']}")
                print(f"Nama Produk: {produk['nama_produk']}")
                print(f"Harga: {produk['harga']}")
                print(f"Jumlah: {produk['quantity']}")
                print(f"Tanggal: {produk['tanggal']}")
                print(f"Pendapatan: {produk['pendapatan']}")
                print("-" * 20)
        
        elif pilihan == "2":
            tanggal_input = input("Masukkan tanggal yang ingin dicari (YYYY-MM-DD): ")
            print(average_penjualan(tanggal_input, data_dengan_pendapatan))
        
        elif pilihan == "3":
            # for total in total_penjualan(data_dengan_pendapatan):
            #     print(total)
            try:
                print(next(total_penjualan_generator))
            except StopIteration:
                print("Semua total penjualan telah ditampilkan.")
        
        elif pilihan == "4":
            print("Keluar dari program.")
            break
        
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

# Jalankan program
main_menu()
