import json
import os
from datetime import datetime, timedelta

# File paths
USERS_FILE = "users.json"
GAMES_FILE = "games.json"
RENTALS_FILE = "rentals.json"

# Helper functions
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_input(prompt, validator=None):
    while True:
        value = input(prompt).strip()
        if validator is None or validator(value):
            return value
        print("Input tidak valid. Silakan coba lagi.")

# User management
def register_user():
    users = load_json(USERS_FILE)
    username = get_input(" ", lambda x: x not in users)
    password = get_input("Masukkan password Anda: ")
    
    users[username] = {
        "password": password,
        "profile": {},
        "friends": []
    }
    save_json(USERS_FILE, users)
    print("Registrasi berhasil!")
    return username

def login():
    users = load_json(USERS_FILE)
    username = get_input("Masukkan username Anda: ")
    password = get_input("Masukkan password Anda: ")
    
    if username in users and users[username]["password"] == password:
        print("Login berhasil!")
        return username
    else:
        print("Username atau password salah.")
        return None

def update_profile(username):
    users = load_json(USERS_FILE)
    print("\nMemperbarui profil:")
    users[username]["profile"]["nama"] = get_input("Masukkan nama Anda: ")
    users[username]["profile"]["umur"] = get_input("Masukkan umur Anda: ", lambda x: x.isdigit())
    users[username]["profile"]["genre_favorit"] = get_input("Masukkan genre game favorit Anda: ")
    save_json(USERS_FILE, users)
    print("Profil berhasil diperbarui!")

def update_friends(username):
    users = load_json(USERS_FILE)
    while True:
        print("\nDaftar teman:", users[username]["friends"])
        action = get_input("Apakah Anda ingin (t)ambah, (h)apus, atau (s)elesai? ").lower()
        if action == 's':
            break
        elif action == 't':
            friend = get_input("Masukkan username teman: ")
            if friend in users and friend not in users[username]["friends"]:
                users[username]["friends"].append(friend)
                print(f"{friend} berhasil ditambahkan ke daftar teman.")
            else:
                print("Username tidak valid atau sudah ada dalam daftar teman.")
        elif action == 'h':
            friend = get_input("Masukkan username teman yang akan dihapus: ")
            if friend in users[username]["friends"]:
                users[username]["friends"].remove(friend)
                print(f"{friend} berhasil dihapus dari daftar teman.")
            else:
                print("Teman tidak ditemukan dalam daftar.")
    save_json(USERS_FILE, users)
    print("Daftar teman berhasil diperbarui!")

# Game management
def add_game():
    games = load_json(GAMES_FILE)
    game_id = get_input("Masukkan ID game: ", lambda x: x not in games)
    title = get_input("Masukkan judul game: ")
    genre = get_input("Masukkan genre game: ")
    price = float(get_input("Masukkan harga sewa per hari: ", lambda x: x.replace('.', '').isdigit()))
    
    games[game_id] = (title, genre, price)
    save_json(GAMES_FILE, games)
    print("Game berhasil ditambahkan!")

def list_games():
    games = load_json(GAMES_FILE)
    print("\nDaftar game yang tersedia:")
    for game_id, (title, genre, price) in games.items():
        print(f"ID: {game_id}, Judul: {title}, Genre: {genre}, Harga/hari: Rp{price:.2f}")

# Rental management
def rent_game(username):
    games = load_json(GAMES_FILE)
    rentals = load_json(RENTALS_FILE)
    
    list_games()
    game_id = get_input("Masukkan ID game yang ingin disewa: ")
    
    if game_id in games:
        if username not in rentals:
            rentals[username] = []
        
        rental_days = int(get_input("Masukkan jumlah hari penyewaan: ", lambda x: x.isdigit() and int(x) > 0))
        start_date = datetime.now()
        end_date = start_date + timedelta(days=rental_days)
        
        rental_info = {
            "game_id": game_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "total_price": games[game_id][2] * rental_days
        }
        
        rentals[username].append(rental_info)
        save_json(RENTALS_FILE, rentals)
        print(f"Game berhasil disewa! Total biaya: Rp{rental_info['total_price']:.2f}")
    else:
        print("Game tidak tersedia.")

def list_rented_games(username):
    rentals = load_json(RENTALS_FILE)
    games = load_json(GAMES_FILE)
    
    if username in rentals:
        print("\nGame yang Anda sewa:")
        for rental in rentals[username]:
            game_id = rental["game_id"]
            title = games[game_id][0]
            print(f"ID: {game_id}, Judul: {title}, Mulai: {rental['start_date']}, Selesai: {rental['end_date']}, Total: Rp{rental['total_price']:.2f}")
    else:
        print("Anda belum menyewa game apapun.")

# Main menu
def main_menu(username):
    while True:
        print("\n--- Menu Utama ---")
        print("1. Perbarui Profil")
        print("2. Perbarui Daftar Teman")
        print("3. Sewa Game")
        print("4. Lihat Game yang Disewa")
        print("5. Lihat Semua Game")
        print("0. Logout")
        
        choice = get_input("Masukkan pilihan Anda: ", lambda x: x.isdigit() and 0 <= int(x) <= 5)
        
        if choice == '0':
            break
        elif choice == '1':
            update_profile(username)
        elif choice == '2':
            update_friends(username)
        elif choice == '3':
            rent_game(username)
        elif choice == '4':
            list_rented_games(username)
        elif choice == '5':
            list_games()

# Main program
def main():
    while True:
        print("\n--- Sistem Penyewaan Game Online ---")
        print("1. Registrasi")
        print("2. Login")
        print("0. Keluar")
        
        choice = get_input("Masukkan pilihan Anda: ", lambda x: x in ['0', '1', '2'])
        
        if choice == '0':
            break
        elif choice == '1':
            username = register_user()
            main_menu(username)
        elif choice == '2':
            username = login()
            if username:
                main_menu(username)

if __name__ == "__main__":
    main()Masukkan username Anda: