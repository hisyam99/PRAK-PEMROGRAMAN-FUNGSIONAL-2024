import json
import os
import getpass
from datetime import datetime, timedelta
from functools import reduce

FILE_PENGGUNA = 'pengguna.json'
FILE_PROFIL = 'profil.json'
FILE_TEMAN = 'teman.json'
FILE_BUKU = 'buku.json'
FILE_PEMINJAMAN = 'peminjaman.json'

KATEGORI = ('Fiksi', 'Non-fiksi', 'Sains', 'Sejarah', 'Biografi')

def muat_data(nama_file):
    if os.path.exists(nama_file):
        with open(nama_file, 'r') as file:
            return json.load(file)
    return {}

def simpan_data(data, nama_file):
    with open(nama_file, 'w') as file:
        json.dump(data, file, indent=4)

def validate_nim(nim):
    return len(nim) == 15 and nim.isdigit()

def create_user_data(nim, password):
    return {
        'pengguna': {nim: password},
        'profil': {nim: {'role': 'user'}},
        'teman': {nim: []}
    }

def daftar(state):
    print("\n=== Pendaftaran ===")
    
    nim = input("Masukkan NIM Anda (15 digit): ")
    if not validate_nim(nim):
        return state, "NIM harus terdiri dari tepat 15 angka. Silakan coba lagi."
    
    if nim in state['pengguna']:
        return state, "NIM sudah terdaftar."
    
    password = getpass.getpass("Masukkan password: ")
    
    new_data = create_user_data(nim, password)
    
    updated_state = {
        'pengguna': {**state['pengguna'], **new_data['pengguna']},
        'profil': {**state['profil'], **new_data['profil']},
        'teman': {**state['teman'], **new_data['teman']},
        'buku': state['buku'],
        'peminjaman': state['peminjaman']
    }
    
    return updated_state, "Pendaftaran berhasil!"

def validate_login(pengguna, nim, password):
    return nim in pengguna and pengguna[nim] == password

def masuk(state):
    print("\n=== Masuk ===")
    nim = input("Masukkan NIM: ")
    password = getpass.getpass("Masukkan password: ")
    
    if validate_login(state['pengguna'], nim, password):
        return nim, "Berhasil masuk!"
    else:
        return None, "NIM atau password salah."

def update_profile(profil, nim, new_data):
    return {**profil, nim: {**profil.get(nim, {}), **new_data}}

def isi_profil(state, nim):
    nama = input("Masukkan nama: ")
    email = input("Masukkan email: ")
    new_data = {'nama': nama, 'email': email}
    updated_profil = update_profile(state['profil'], nim, new_data)
    updated_state = {**state, 'profil': updated_profil}
    return updated_state, "Profil berhasil diperbarui!"

def add_friend(teman, nim, nim_teman):
    if nim not in teman:
        return teman, f"Pengguna dengan NIM {nim} tidak ditemukan."
    
    updated_friends = teman[nim] + [nim_teman]
    return {**teman, nim: updated_friends}, f"Teman dengan NIM {nim_teman} berhasil ditambahkan!"

def tambah_teman(state, nim):
    teman = state['teman']
    pengguna = state['pengguna']
    while True:
        nim_teman = input("Masukkan NIM teman (atau tekan enter untuk selesai): ")
        if nim_teman == "":
            break
        
        if nim_teman in pengguna:
            teman, message = add_friend(teman, nim, nim_teman)
            print(message)
        else:
            print(f"Tidak ada pengguna dengan NIM {nim_teman}.")
    
    updated_state = {**state, 'teman': teman}
    return updated_state, "Proses menambahkan teman selesai."

def lihat_profil(state, nim):
    print("\n=== Profil Anda ===")
    profil = state['profil'].get(nim, {})
    for key, value in profil.items():
        print(f"{key.capitalize()}: {value}")
    return state, ""

def lihat_teman(state, nim):
    print("\n=== Daftar Teman Anda ===")
    teman_list = state['teman'].get(nim, [])
    for nim_teman in teman_list:
        nama_teman = state['profil'].get(nim_teman, {}).get('nama', "Tidak dikenal")
        print(f"NIM: {nim_teman}, Nama: {nama_teman}")
    return state, ""

def hapus_teman(state, nim):
    teman_list = state['teman'].get(nim, [])
    if not teman_list:
        return state, "Anda tidak memiliki teman untuk dihapus."
    
    print("\n=== Hapus Teman ===")
    for i, nim_teman in enumerate(teman_list, 1):
        nama_teman = state['profil'].get(nim_teman, {}).get('nama', "Tidak dikenal")
        print(f"{i}. NIM: {nim_teman}, Nama: {nama_teman}")
    
    pilihan = int(input("Masukkan nomor teman yang ingin dihapus: ")) - 1
    if 0 <= pilihan < len(teman_list):
        nim_teman_dihapus = teman_list.pop(pilihan)
        updated_teman = {**state['teman'], nim: teman_list}
        updated_state = {**state, 'teman': updated_teman}
        return updated_state, f"Teman dengan NIM {nim_teman_dihapus} telah dihapus dari daftar teman Anda."
    else:
        return state, "Pilihan tidak valid."

def tambah_buku(state):
    print("\n=== Tambah Buku ===")
    isbn = input("Masukkan ISBN: ")
    if isbn in state['buku']:
        return state, "Buku dengan ISBN ini sudah ada."
    
    judul = input("Masukkan judul: ")
    penulis = input("Masukkan penulis: ")
    print("Kategori yang tersedia:")
    for i, kategori in enumerate(KATEGORI, 1):
        print(f"{i}. {kategori}")
    pilihan_kategori = int(input("Pilih nomor kategori: ")) - 1
    kategori = KATEGORI[pilihan_kategori] if 0 <= pilihan_kategori < len(KATEGORI) else 'Fiksi'
    jumlah = int(input("Masukkan jumlah: "))
    
    new_book = {'judul': judul, 'penulis': penulis, 'kategori': kategori, 'jumlah': jumlah}
    updated_buku = {**state['buku'], isbn: new_book}
    updated_state = {**state, 'buku': updated_buku}
    return updated_state, "Buku berhasil ditambahkan!"

def lihat_buku(state):
    print("\n=== Buku yang Tersedia ===")
    for isbn, info in state['buku'].items():
        print(f"ISBN: {isbn}")
        for key, value in info.items():
            print(f"  {key.capitalize()}: {value}")
        print()
    return state, ""

def pinjam_buku(state, nim):
    print("\n=== Pinjam Buku ===")
    lihat_buku(state)
    isbn = input("Masukkan ISBN buku yang ingin dipinjam: ")
    if isbn not in state['buku']:
        return state, "Buku tidak ditemukan."
    
    if state['buku'][isbn]['jumlah'] <= 0:
        return state, "Maaf, buku ini sedang tidak tersedia."
    
    updated_buku = {
        **state['buku'],
        isbn: {**state['buku'][isbn], 'jumlah': state['buku'][isbn]['jumlah'] - 1}
    }
    
    id_pinjam = f"{nim}-{isbn}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    tanggal_kembali = datetime.now() + timedelta(days=14)
    new_peminjaman = {
        id_pinjam: {
            'nim': nim,
            'isbn': isbn,
            'tanggal_pinjam': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tanggal_kembali': tanggal_kembali.strftime('%Y-%m-%d %H:%M:%S'),
            'dikembalikan': False
        }
    }
    
    updated_peminjaman = {**state['peminjaman'], **new_peminjaman}
    updated_state = {**state, 'buku': updated_buku, 'peminjaman': updated_peminjaman}
    return updated_state, f"Anda telah meminjam '{state['buku'][isbn]['judul']}'. Harap kembalikan sebelum {tanggal_kembali.strftime('%Y-%m-%d')}."

def kembalikan_buku(state, nim):
    print("\n=== Kembalikan Buku ===")
    pinjaman_pengguna = [
        (id_pinjam, pinjam) for id_pinjam, pinjam in state['peminjaman'].items()
        if pinjam['nim'] == nim and not pinjam['dikembalikan']
    ]
    if not pinjaman_pengguna:
        return state, "Anda tidak memiliki buku untuk dikembalikan."
    
    for i, (id_pinjam, pinjam) in enumerate(pinjaman_pengguna, 1):
        print(f"{i}. '{state['buku'][pinjam['isbn']]['judul']}' (Tenggat: {pinjam['tanggal_kembali']})")
    
    pilihan = int(input("Masukkan nomor buku yang ingin dikembalikan: ")) - 1
    if 0 <= pilihan < len(pinjaman_pengguna):
        id_pinjam, pinjam = pinjaman_pengguna[pilihan]
        updated_peminjaman = {
            **state['peminjaman'],
            id_pinjam: {**pinjam, 'dikembalikan': True}
        }
        updated_buku = {
            **state['buku'],
            pinjam['isbn']: {
                **state['buku'][pinjam['isbn']],
                'jumlah': state['buku'][pinjam['isbn']]['jumlah'] + 1
            }
        }
        updated_state = {**state, 'peminjaman': updated_peminjaman, 'buku': updated_buku}
        return updated_state, f"Anda telah berhasil mengembalikan '{state['buku'][pinjam['isbn']]['judul']}'."
    else:
        return state, "Pilihan tidak valid."

def lihat_peminjaman(state, nim):
    print("\n=== Peminjaman Anda ===")
    pinjaman_pengguna = [
        pinjam for pinjam in state['peminjaman'].values()
        if pinjam['nim'] == nim
    ]
    if not pinjaman_pengguna:
        return state, "Anda tidak memiliki riwayat peminjaman."
    
    for pinjam in pinjaman_pengguna:
        print(f"Buku: '{state['buku'][pinjam['isbn']]['judul']}'")
        print(f"  Dipinjam: {pinjam['tanggal_pinjam']}")
        print(f"  Tenggat: {pinjam['tanggal_kembali']}")
        print(f"  Status: {'Dikembalikan' if pinjam['dikembalikan'] else 'Belum dikembalikan'}")
        print()
    return state, ""

def lihat_semua_peminjaman(state):
    print("\n=== Semua Peminjaman ===")
    if not state['peminjaman']:
        return state, "Tidak ada peminjaman dalam sistem."
    
    for id_pinjam, pinjam in state['peminjaman'].items():
        print(f"ID Peminjaman: {id_pinjam}")
        print(f"Pengguna: {state['profil'][pinjam['nim']]['nama']} (NIM: {pinjam['nim']})")
        print(f"Buku: '{state['buku'][pinjam['isbn']]['judul']}'")
        print(f"Dipinjam: {pinjam['tanggal_pinjam']}")
        print(f"Tenggat: {pinjam['tanggal_kembali']}")
        print(f"Status: {'Dikembalikan' if pinjam['dikembalikan'] else 'Belum dikembalikan'}")
        print()
    return state, ""

def menu_pengguna(state, nim):
    while True:
        print("\n=== Menu Pengguna ===")
        print("1. Lihat Profil")
        print("2. Edit Profil")
        print("3. Lihat Teman")
        print("4. Tambah Teman")
        print("5. Hapus Teman")
        print("6. Lihat Buku Tersedia")
        print("7. Pinjam Buku")
        print("8. Kembalikan Buku")
        print("9. Lihat Peminjaman Saya")
        print("10. Keluar")
        
        pilihan = input("Masukkan pilihan Anda: ")
        
        if pilihan == '1':
            state, _ = lihat_profil(state, nim)
        elif pilihan == '2':
            state, message = isi_profil(state, nim)
            print(message)
        elif pilihan == '3':
            state, _ = lihat_teman(state, nim)
        elif pilihan == '4':
            state, message = tambah_teman(state, nim)
            print(message)
        elif pilihan == '5':
            state, message = hapus_teman(state, nim)
            print(message)
        elif pilihan == '6':
            state, _ = lihat_buku(state)
        elif pilihan == '7':
            state, message = pinjam_buku(state, nim)
            print(message)
        elif pilihan == '8':
            state, message = kembalikan_buku(state, nim)
            print(message)
        elif pilihan == '9':
            state, _ = lihat_peminjaman(state, nim)
        elif pilihan == '10':
            print("Keluar dari akun...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    return state

def menu_admin(state):
    while True:
        print("\n=== Menu admin ===")
        print("1. Tambah Buku")
        print("2. Lihat Buku")
        print("3. Lihat Semua Peminjaman")
        print("4. Keluar")
        
        pilihan = input("Masukkan pilihan Anda: ")
        
        if pilihan == '1':
            state, message = tambah_buku(state)
            print(message)
        elif pilihan == '2':
            state, _ = lihat_buku(state)
        elif pilihan == '3':
            state, _ = lihat_semua_peminjaman(state)
        elif pilihan == '4':
            print("Keluar dari akun admin...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    return state

def main():
    state = {
        'pengguna': muat_data(FILE_PENGGUNA),
        'profil': muat_data(FILE_PROFIL),
        'teman': muat_data(FILE_TEMAN),
        'buku': muat_data(FILE_BUKU),
        'peminjaman': muat_data(FILE_PEMINJAMAN)
    }

    while True:
        print("\n=== Sistem Manajemen Perpustakaan ===")
        print("1. Daftar")
        print("2. Masuk")
        print("3. Keluar")
        
        pilihan = input("Masukkan pilihan Anda: ")
        
        if pilihan == '1':
            state, message = daftar(state)
            print(message)
        elif pilihan == '2':
            nim, message = masuk(state)
            print(message)
            if nim:
                if state['profil'][nim]['role'] == 'admin':
                    state = menu_admin(state)
                else:
                    state = menu_pengguna(state, nim)
        elif pilihan == '3':
            print("Terima kasih telah menggunakan Sistem Manajemen Perpustakaan. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    
    # Simpan semua data sebelum keluar
    simpan_data(state['pengguna'], FILE_PENGGUNA)
    simpan_data(state['profil'], FILE_PROFIL)
    simpan_data(state['teman'], FILE_TEMAN)
    simpan_data(state['buku'], FILE_BUKU)
    simpan_data(state['peminjaman'], FILE_PEMINJAMAN)

if __name__ == "__main__":
    main()