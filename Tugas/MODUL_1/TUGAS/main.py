import json
import os
import getpass
from datetime import datetime, timedelta

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

pengguna = muat_data(FILE_PENGGUNA)
profil = muat_data(FILE_PROFIL)
teman = muat_data(FILE_TEMAN)
buku = muat_data(FILE_BUKU)
peminjaman = muat_data(FILE_PEMINJAMAN)

def daftar():
    print("\n=== Pendaftaran ===")
    
    while True:
        nim = input("Masukkan NIM Anda (15 digit): ")
        if len(nim) == 15 and nim.isdigit(): 
            break
        else:
            print("NIM harus terdiri dari tepat 15 angka. Silakan coba lagi.")
    
    if nim in pengguna:
        print("NIM sudah terdaftar.")
        return
    
    password = getpass.getpass("Masukkan password: ")
    
    pengguna[nim] = password
    profil[nim] = {
        'role': 'user'
    }
    teman[nim] = []
    
    simpan_data(pengguna, FILE_PENGGUNA)
    simpan_data(profil, FILE_PROFIL)
    simpan_data(teman, FILE_TEMAN)
    
    print("Pendaftaran berhasil!")
    
    if input("Apakah Anda ingin mengisi profil sekarang? (y/n): ").lower() == 'y':
        isi_profil(nim)
    else:
        print("Anda dapat mengisi profil nanti.")


def masuk():
    print("\n=== Masuk ===")
    nim = input("Masukkan NIM: ")
    password = getpass.getpass("Masukkan password: ")
    if nim in pengguna and pengguna[nim] == password:
        print("Berhasil masuk!")
        return nim
    else:
        print("NIM atau password salah.")
        return None

def isi_profil(nim):
    profil[nim]['nama'] = input("Masukkan nama: ")
    profil[nim]['email'] = input("Masukkan email: ")
    # profil[nim]['role'] = input("Masukkan role (user/admin): ").lower()
    # if profil[nim]['role'] not in ['user', 'admin']:
    #     profil[nim]['role'] = 'user'
    simpan_data(profil, FILE_PROFIL)
    print("Profil berhasil diperbarui!")

def tambah_teman(nim):
    while True:
        nim_teman = input("Masukkan NIM teman (atau tekan enter untuk selesai): ")
        if nim_teman == "":
            break
        if nim_teman in pengguna:
            teman[nim].append(nim_teman)
            print(f"Teman dengan NIM {nim_teman} berhasil ditambahkan!")
        else:
            print(f"Tidak ada pengguna dengan NIM {nim_teman}.")
    simpan_data(teman, FILE_TEMAN)
    print("Proses menambahkan teman selesai.")

def menu_pengguna(nim):
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
            lihat_profil(nim)
        elif pilihan == '2':
            isi_profil(nim)
        elif pilihan == '3':
            lihat_teman(nim)
        elif pilihan == '4':
            tambah_teman(nim)
        elif pilihan == '5':
            hapus_teman(nim)
        elif pilihan == '6':
            lihat_buku()
        elif pilihan == '7':
            pinjam_buku(nim)
        elif pilihan == '8':
            kembalikan_buku(nim)
        elif pilihan == '9':
            lihat_peminjaman(nim)
        elif pilihan == '10':
            print("Keluar dari akun...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def lihat_profil(nim):
    print("\n=== Profil Anda ===")
    for key, value in profil[nim].items():
        print(f"{key.capitalize()}: {value}")

def lihat_teman(nim):
    print("\n=== Daftar Teman Anda ===")
    for nim_teman in teman[nim]:
        nama_teman = profil[nim_teman]['nama'] if nim_teman in profil else "Tidak dikenal"
        print(f"NIM: {nim_teman}, Nama: {nama_teman}")

def hapus_teman(nim):
    print("\n=== Hapus Teman ===")
    if teman[nim]:
        for i, nim_teman in enumerate(teman[nim], 1):
            nama_teman = profil[nim_teman]['nama'] if nim_teman in profil else "Tidak dikenal"
            print(f"{i}. NIM: {nim_teman}, Nama: {nama_teman}")
        pilihan = int(input("Masukkan nomor teman yang ingin dihapus: ")) - 1
        if 0 <= pilihan < len(teman[nim]):
            nim_teman_dihapus = teman[nim].pop(pilihan)
            simpan_data(teman, FILE_TEMAN)
            print(f"Teman dengan NIM {nim_teman_dihapus} telah dihapus dari daftar teman Anda.")
        else:
            print("Pilihan tidak valid.")
    else:
        print("Anda tidak memiliki teman untuk dihapus.")

def tambah_buku():
    print("\n=== Tambah Buku ===")
    isbn = input("Masukkan ISBN: ")
    if isbn in buku:
        print("Buku dengan ISBN ini sudah ada.")
        return
    judul = input("Masukkan judul: ")
    penulis = input("Masukkan penulis: ")
    print("Kategori yang tersedia:")
    for i, kategori in enumerate(KATEGORI, 1):
        print(f"{i}. {kategori}")
    pilihan_kategori = int(input("Pilih nomor kategori: ")) - 1
    if 0 <= pilihan_kategori < len(KATEGORI):
        kategori = KATEGORI[pilihan_kategori]
    else:
        print("Kategori tidak valid. Menetapkan ke 'Fiksi'.")
        kategori = 'Fiksi'
    jumlah = int(input("Masukkan jumlah: "))
    buku[isbn] = {'judul': judul, 'penulis': penulis, 'kategori': kategori, 'jumlah': jumlah}
    simpan_data(buku, FILE_BUKU)
    print("Buku berhasil ditambahkan!")

def lihat_buku():
    print("\n=== Buku yang Tersedia ===")
    for isbn, info in buku.items():
        print(f"ISBN: {isbn}")
        for key, value in info.items():
            print(f"  {key.capitalize()}: {value}")
        print()

def pinjam_buku(nim):
    print("\n=== Pinjam Buku ===")
    lihat_buku()
    isbn = input("Masukkan ISBN buku yang ingin dipinjam: ")
    if isbn in buku:
        if buku[isbn]['jumlah'] > 0:
            buku[isbn]['jumlah'] -= 1
            id_pinjam = f"{nim}-{isbn}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            tanggal_kembali = datetime.now() + timedelta(days=14)
            peminjaman[id_pinjam] = {
                'nim': nim,
                'isbn': isbn,
                'tanggal_pinjam': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tanggal_kembali': tanggal_kembali.strftime('%Y-%m-%d %H:%M:%S'),
                'dikembalikan': False
            }
            simpan_data(buku, FILE_BUKU)
            simpan_data(peminjaman, FILE_PEMINJAMAN)
            print(f"Anda telah meminjam '{buku[isbn]['judul']}'. Harap kembalikan sebelum {tanggal_kembali.strftime('%Y-%m-%d')}.")
        else:
            print("Maaf, buku ini sedang tidak tersedia.")
    else:
        print("Buku tidak ditemukan.")

def kembalikan_buku(nim):
    print("\n=== Kembalikan Buku ===")
    pinjaman_pengguna = [pinjam for id_pinjam, pinjam in peminjaman.items() if pinjam['nim'] == nim and not pinjam['dikembalikan']]
    if not pinjaman_pengguna:
        print("Anda tidak memiliki buku untuk dikembalikan.")
        return
    for i, pinjam in enumerate(pinjaman_pengguna, 1):
        print(f"{i}. '{buku[pinjam['isbn']]['judul']}' (Tenggat: {pinjam['tanggal_kembali']})")
    pilihan = int(input("Masukkan nomor buku yang ingin dikembalikan: ")) - 1
    if 0 <= pilihan < len(pinjaman_pengguna):
        pinjam = pinjaman_pengguna[pilihan]
        id_pinjam = [id for id, p in peminjaman.items() if p == pinjam][0]
        peminjaman[id_pinjam]['dikembalikan'] = True
        buku[pinjam['isbn']]['jumlah'] += 1
        simpan_data(peminjaman, FILE_PEMINJAMAN)
        simpan_data(buku, FILE_BUKU)
        print(f"Anda telah berhasil mengembalikan '{buku[pinjam['isbn']]['judul']}'.")
    else:
        print("Pilihan tidak valid.")

def lihat_peminjaman(nim):
    print("\n=== Peminjaman Anda ===")
    pinjaman_pengguna = [pinjam for pinjam in peminjaman.values() if pinjam['nim'] == nim]
    if not pinjaman_pengguna:
        print("Anda tidak memiliki riwayat peminjaman.")
        return
    for pinjam in pinjaman_pengguna:
        print(f"Buku: '{buku[pinjam['isbn']]['judul']}'")
        print(f"  Dipinjam: {pinjam['tanggal_pinjam']}")
        print(f"  Tenggat: {pinjam['tanggal_kembali']}")
        print(f"  Status: {'Dikembalikan' if pinjam['dikembalikan'] else 'Belum dikembalikan'}")
        print()

def menu_admin(nim):
    while True:
        print("\n=== Menu admin ===")
        print("1. Tambah Buku")
        print("2. Lihat Buku")
        print("3. Lihat Semua Peminjaman")
        print("4. Keluar")
        
        pilihan = input("Masukkan pilihan Anda: ")
        
        if pilihan == '1':
            tambah_buku()
        elif pilihan == '2':
            lihat_buku()
        elif pilihan == '3':
            lihat_semua_peminjaman()
        elif pilihan == '4':
            print("Keluar dari akun admin...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def lihat_semua_peminjaman():
    print("\n=== Semua Peminjaman ===")
    if not peminjaman:
        print("Tidak ada peminjaman dalam sistem.")
        return
    for id_pinjam, pinjam in peminjaman.items():
        print(f"ID Peminjaman: {id_pinjam}")
        print(f"Pengguna: {profil[pinjam['nim']]['nama']} (NIM: {pinjam['nim']})")
        print(f"Buku: '{buku[pinjam['isbn']]['judul']}'")
        print(f"Dipinjam: {pinjam['tanggal_pinjam']}")
        print(f"Tenggat: {pinjam['tanggal_kembali']}")
        print(f"Status: {'Dikembalikan' if pinjam['dikembalikan'] else 'Belum dikembalikan'}")
        print()

def main():
    while True:
        print("\n=== Sistem Manajemen Perpustakaan ===")
        print("1. Daftar")
        print("2. Masuk")
        print("3. Keluar")
        
        pilihan = input("Masukkan pilihan Anda: ")
        
        if pilihan == '1':
            daftar()
        elif pilihan == '2':
            nim = masuk()
            if nim:
                if profil[nim]['role'] == 'admin':
                    menu_admin(nim)
                else:
                    menu_pengguna(nim)
        elif pilihan == '3':
            print("Terima kasih telah menggunakan Sistem Manajemen Perpustakaan. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()