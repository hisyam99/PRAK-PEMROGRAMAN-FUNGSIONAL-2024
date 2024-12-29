import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Data pengguna
users = [
    {"id": 1, "name": "Agus", "age": 26, "gender": "Laki-laki", "city": "Surabaya"},
    {"id": 2, "name": "Budi", "age": 25, "gender": "Laki-laki", "city": "Malang"},
    {"id": 3, "name": "Citra", "age": 19, "gender": "Perempuan", "city": "Kediri"},
    {"id": 4, "name": "Dewi", "age": 20, "gender": "Perempuan", "city": "Sidoarjo"},
    {"id": 5, "name": "Eka", "age": 16, "gender": "Perempuan", "city": "Malang"},
    {"id": 6, "name": "Fajar", "age": 28, "gender": "Laki-laki", "city": "Surabaya"},
    {"id": 7, "name": "Gita", "age": 19, "gender": "Perempuan", "city": "Malang"},
    {"id": 8, "name": "Hendra", "age": 29, "gender": "Laki-laki", "city": "Kediri"},
    {"id": 9, "name": "Indah", "age": 20, "gender": "Perempuan", "city": "Sidoarjo"},
    {"id": 10, "name": "Joko", "age": 26, "gender": "Laki-laki", "city": "Blitar"},
    {"id": 11, "name": "Kirana", "age": 19, "gender": "Perempuan", "city": "Surabaya"},
    {"id": 12, "name": "Lina", "age": 18, "gender": "Perempuan", "city": "Malang"},
    {"id": 13, "name": "Maya", "age": 17, "gender": "Perempuan", "city": "Kediri"},
    {"id": 14, "name": "Nanda", "age": 26, "gender": "Laki-laki", "city": "Sidoarjo"},
    {"id": 15, "name": "Oki", "age": 25, "gender": "Laki-laki", "city": "Malang"},
    {"id": 16, "name": "Putri", "age": 19, "gender": "Perempuan", "city": "Surabaya"},
    {"id": 17, "name": "Rian", "age": 30, "gender": "Laki-laki", "city": "Malang"},
    {"id": 18, "name": "Siti", "age": 18, "gender": "Perempuan", "city": "Kediri"},
    {"id": 19, "name": "Taufik", "age": 27, "gender": "Laki-laki", "city": "Sidoarjo"},
    {"id": 20, "name": "Umi", "age": 20, "gender": "Perempuan", "city": "Blitar"},
    {"id": 21, "name": "Vina", "age": 17, "gender": "Perempuan", "city": "Surabaya"},
    {"id": 22, "name": "Wawan", "age": 29, "gender": "Laki-laki", "city": "Malang"},
    {"id": 23, "name": "Yuni", "age": 16, "gender": "Perempuan", "city": "Kediri"},
    {"id": 24, "name": "Zainal", "age": 28, "gender": "Laki-laki", "city": "Sidoarjo"},
    {"id": 25, "name": "Adi", "age": 26, "gender": "Laki-laki", "city": "Blitar"},
    {"id": 26, "name": "Bella", "age": 18, "gender": "Perempuan", "city": "Surabaya"},
    {"id": 27, "name": "Cindy", "age": 19, "gender": "Perempuan", "city": "Malang"},
    {"id": 28, "name": "Doni", "age": 30, "gender": "Laki-laki", "city": "Kediri"},
    {"id": 29, "name": "Eris", "age": 27, "gender": "Laki-laki", "city": "Sidoarjo"},
    {"id": 30, "name": "Fani", "age": 16, "gender": "Perempuan", "city": "Blitar"}
]

# Data buku
books = [
    {"id": 1, "title": "Python Dasar", "pages": 320, "genre": "Pemrograman"},
    {"id": 2, "title": "Python Lanjutan", "pages": 450, "genre": "Pemrograman"},
    {"id": 3, "title": "Panduan Data Science", "pages": 520, "genre": "Data Science"},
    {"id": 4, "title": "Pembelajaran Mesin", "pages": 600, "genre": "AI"},
    {"id": 5, "title": "Deep Learning", "pages": 720, "genre": "AI"},
]

# Data peminjaman buku (fluktuatif)
borrowings = [
    {"user_id": 1, "book_id": 1, "borrow_date": "2024-11-20"},
    {"user_id": 2, "book_id": 3, "borrow_date": "2024-11-21"},
    {"user_id": 3, "book_id": 5, "borrow_date": "2024-11-21"},
    {"user_id": 4, "book_id": 2, "borrow_date": "2024-11-22"},
    {"user_id": 5, "book_id": 4, "borrow_date": "2024-11-23"},
    {"user_id": 6, "book_id": 4, "borrow_date": "2024-11-23"},
    {"user_id": 7, "book_id": 3, "borrow_date": "2024-11-24"},
    {"user_id": 8, "book_id": 4, "borrow_date": "2024-11-24"},
    {"user_id": 9, "book_id": 5, "borrow_date": "2024-11-24"},
    {"user_id": 10, "book_id": 2, "borrow_date": "2024-11-25"},
    {"user_id": 11, "book_id": 4, "borrow_date": "2024-11-25"},
    {"user_id": 12, "book_id": 3, "borrow_date": "2024-11-26"},
    {"user_id": 13, "book_id": 4, "borrow_date": "2024-11-27"},
    {"user_id": 14, "book_id": 5, "borrow_date": "2024-11-27"},
    {"user_id": 15, "book_id": 2, "borrow_date": "2024-11-28"},
    {"user_id": 16, "book_id": 1, "borrow_date": "2024-11-28"},
    {"user_id": 17, "book_id": 3, "borrow_date": "2024-11-29"},
    {"user_id": 18, "book_id": 4, "borrow_date": "2024-11-30"},
    {"user_id": 19, "book_id": 5, "borrow_date": "2024-11-30"},
    {"user_id": 20, "book_id": 2, "borrow_date": "2024-11-30"},
    {"user_id": 21, "book_id": 1, "borrow_date": "2024-12-01"},
    {"user_id": 22, "book_id": 3, "borrow_date": "2024-12-02"},
    {"user_id": 23, "book_id": 4, "borrow_date": "2024-12-02"},
    {"user_id": 24, "book_id": 5, "borrow_date": "2024-12-03"},
    {"user_id": 25, "book_id": 2, "borrow_date": "2024-12-03"},
    {"user_id": 26, "book_id": 1, "borrow_date": "2024-12-03"},
    {"user_id": 27, "book_id": 3, "borrow_date": "2024-12-04"},
    {"user_id": 28, "book_id": 4, "borrow_date": "2024-12-04"},
    {"user_id": 29, "book_id": 5, "borrow_date": "2024-12-05"},
    {"user_id": 30, "book_id": 2, "borrow_date": "2024-12-06"},
]

# Memproses data untuk visualisasi
# Mendapatkan daftar usia pengguna
user_ages = [user["age"] for user in users]

# Mendapatkan daftar kota pengguna
user_cities = [user["city"] for user in users]

# Mendapatkan judul buku
book_titles = [book["title"] for book in books]

# Mendapatkan jumlah halaman buku
book_pages = [book["pages"] for book in books]

# Mendapatkan genre buku
book_genres = [book["genre"] for book in books]

# Menghitung jumlah peminjaman berdasarkan buku dan genre
genre_count = {genre: 0 for genre in set(book_genres)}
for b in borrowings:
    book = next(book for book in books if book["id"] == b["book_id"])
    genre_count[book["genre"]] += 1  # Menambah jumlah peminjaman untuk genre ini

# Menghitung peminjaman berdasarkan kota
borrow_by_city = {city: 0 for city in set(user_cities)}
for b in borrowings:
    user = next(user for user in users if user["id"] == b["user_id"])
    borrow_by_city[user["city"]] += 1  # Menambah jumlah peminjaman untuk kota ini

# Menghitung rata rata umur tiap gender
average_age_by_gender = {
    "Laki-laki": np.mean([user["age"] for user in users if user["gender"] == "Laki-laki"]),
    "Perempuan": np.mean([user["age"] for user in users if user["gender"] == "Perempuan"]),
}

# Data peminjaman per hari
borrow_dates = [datetime.strptime(b["borrow_date"], "%Y-%m-%d") for b in borrowings]
borrow_dates.sort()

# Mengonversi tanggal ke string untuk pengelompokan
date_strings = [date.strftime("%Y-%m-%d") for date in borrow_dates]

# Mendapatkan daftar unik tanggal dan jumlah peminjaman per hari
unique_dates, borrow_counts_per_day = np.unique(date_strings, return_counts=True)

# Konversi kembali ke datetime untuk visualisasi
unique_dates = [datetime.strptime(date, "%Y-%m-%d") for date in unique_dates]

# Membuat visualisasi
plt.figure(figsize=(18, 14))  # Mengatur ukuran plot keseluruhan

# Scatter plot untuk usia pengguna
plt.subplot(3, 3, 1)
scatter_colors = [plt.cm.viridis(age / max(user_ages)) for age in user_ages]
plt.scatter(range(len(users)), user_ages, color=scatter_colors, edgecolor="black", s=80)
plt.title("Scatter Plot Usia Pengguna", fontsize=12)
plt.xlabel("Indeks Pengguna", fontsize=10)
plt.ylabel("Usia", fontsize=10)

# Bar plot untuk peminjaman berdasarkan kota
plt.subplot(3, 3, 2)
plt.bar(borrow_by_city.keys(), borrow_by_city.values(), color="purple", alpha=0.8)
plt.title("Peminjaman Berdasarkan Kota", fontsize=12)
plt.xlabel("Kota", fontsize=10)
plt.ylabel("Jumlah Peminjaman", fontsize=10)

# Line plot jumlah halaman buku
plt.subplot(3, 3, 3)
plt.plot(book_titles, book_pages, color="orange", linestyle="--", marker="o", linewidth=2)
plt.title("Jumlah Halaman Buku", fontsize=12)
plt.xlabel("Judul Buku", fontsize=10)
plt.ylabel("Jumlah Halaman", fontsize=10)
plt.xticks(fontsize=8, rotation=90)

# Menentukan genre dengan jumlah peminjaman terbesar
max_genre_index = list(genre_count.values()).index(max(genre_count.values()))

# Membuat explode untuk menonjolkan genre dengan nilai terbesar
explode = [0.1 if i == max_genre_index else 0 for i in range(len(genre_count))]

# Membuat Pie Chart dengan explode
plt.subplot(3, 3, 4)
plt.pie(
    genre_count.values(),
    labels=genre_count.keys(),
    autopct="%1.1f%%",
    colors=plt.cm.Set3.colors,
    shadow=True,
    startangle=140,
    textprops={"fontsize": 9},
    explode=explode,  # Menambahkan explode
)
plt.title("Peminjaman Berdasarkan Genre", fontsize=12)


# Grafik tren peminjaman dari waktu ke waktu
plt.subplot(3, 3, 5)
borrow_dates = [datetime.strptime(b["borrow_date"], "%Y-%m-%d") for b in borrowings]
borrow_dates.sort()  # Mengurutkan tanggal peminjaman
borrow_counts_over_time = range(1, len(borrow_dates) + 1)
plt.plot(borrow_dates, borrow_counts_over_time, color="green", marker="o", linestyle="-", linewidth=2)
plt.title("Tren Peminjaman dari Waktu ke Waktu", fontsize=12)
plt.xlabel("Tanggal", fontsize=10)
plt.ylabel("Jumlah Peminjaman Kumulatif", fontsize=10)
plt.xticks(rotation=90, fontsize=8)

# Bar plot rata-rata usia berdasarkan gender
plt.subplot(3, 3, 6)
plt.bar(
    average_age_by_gender.keys(),
    average_age_by_gender.values(),
    color=["blue", "pink"],
    alpha=0.8,
)
plt.title("Rata-rata Usia Berdasarkan Gender", fontsize=12)
plt.xlabel("Gender", fontsize=10)
plt.ylabel("Rata-rata Usia", fontsize=10)

# Grafik tren peminjaman per hari
plt.subplot(3, 3, 7)
plt.plot(unique_dates, borrow_counts_per_day, color="blue", marker="o", linestyle="-", linewidth=2)
plt.title("Tren Peminjaman Per Hari", fontsize=12)
plt.xlabel("Tanggal", fontsize=10)
plt.ylabel("Jumlah Peminjaman", fontsize=10)
plt.xticks(rotation=90, fontsize=8)
plt.grid(True)

# Mengatur jarak antar subplot
plt.tight_layout()
plt.show()
