# Tugas 2

import pandas as pd
from functools import reduce

# Load the dataset
file_path = 'dataset.csv'
data = pd.read_csv(file_path)

# Define functions for each operation
def rata_rata_harga_per_tahun(data):
    # Extract year from the date and group data
    data['year'] = pd.to_datetime(data['date']).dt.year
    return data.groupby(['year', 'item'])['price'].mean().reset_index()

def harga_tertinggi_dan_terendah(data):
    # Find the rows with max and min prices
    max_price = data.loc[data['price'].idxmax()]
    min_price = data.loc[data['price'].idxmin()]
    return max_price, min_price

def sortir_berdasarkan_harga(data, lower_bound, upper_bound):
    # Filter rows based on price range
    return data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)]

# Execute operations
rata_rata_harga_pertahun = rata_rata_harga_per_tahun(data)
harga_tinggi_dan_terendah = harga_tertinggi_dan_terendah(data)
sortir_harga = sortir_berdasarkan_harga(data, 1.50, 2.35)

# Display results
print("=== Rata-rata Harga Per Tahun ===")
print(rata_rata_harga_pertahun.head())  # Show first 5 results

print("\n=== Produk dengan Harga Tertinggi ===")
print(harga_tinggi_dan_terendah[0])

print("\n=== Produk dengan Harga Terendah ===")
print(harga_tinggi_dan_terendah[1])

print("\n=== Produk dengan Harga antara 1.50 dan 2.35 ===")
print(sortir_harga.head())  # Show first 5 results