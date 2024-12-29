import json
import os
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
    try:
        with open(nama_file, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        return False

def validate_nim(nim):
    return len(nim) == 15 and nim.isdigit()

def create_user_data(nim, password):
    return {
        'pengguna': {nim: password},
        'profil': {nim: {'role': 'user'}},
        'teman': {nim: []}
    }

def daftar(state, nim, password):
    if not validate_nim(nim):
        return state, False
    
    if nim in state['pengguna']:
        return state, False
    
    new_data = create_user_data(nim, password)
    updated_state = {
        'pengguna': {**state['pengguna'], **new_data['pengguna']},
        'profil': {**state['profil'], **new_data['profil']},
        'teman': {**state['teman'], **new_data['teman']},
        'buku': state['buku'],
        'peminjaman': state['peminjaman']
    }
    return updated_state, True

def validate_login(pengguna, nim, password):
    return nim in pengguna and pengguna[nim] == password

def masuk(state, nim, password):
    if validate_login(state['pengguna'], nim, password):
        return nim
    return None

def isi_profil(state, nim, nama, email):
    new_data = {'nama': nama, 'email': email}
    updated_profil = {**state['profil'], nim: {**state['profil'].get(nim, {}), **new_data}}
    updated_state = {**state, 'profil': updated_profil}
    return updated_state

def tambah_teman(state, nim, nim_teman):
    if nim_teman in state['pengguna']:
        teman_list = state['teman'][nim] + [nim_teman]
        updated_state = {**state, 'teman': {**state['teman'], nim: teman_list}}
        return updated_state, True
    return state, False

def hapus_teman(state, nim, pilihan):
    teman_list = state['teman'].get(nim, [])
    if not teman_list or not (0 <= pilihan < len(teman_list)):
        return state, False
    
    nim_teman_dihapus = teman_list.pop(pilihan)
    updated_state = {**state, 'teman': {**state['teman'], nim: teman_list}}
    return updated_state, True

def tambah_buku(state, isbn, judul, penulis, kategori, jumlah):
    if isbn in state['buku']:
        return state, False
    new_book = {'judul': judul, 'penulis': penulis, 'kategori': kategori, 'jumlah': jumlah}
    updated_state = {**state, 'buku': {**state['buku'], isbn: new_book}}
    return updated_state, True

def pinjam_buku(state, nim, isbn):
    if isbn not in state['buku'] or state['buku'][isbn]['jumlah'] <= 0:
        return state, False
    
    updated_buku = {**state['buku'], isbn: {**state['buku'][isbn], 'jumlah': state['buku'][isbn]['jumlah'] - 1}}
    id_pinjam = f"{nim}-{isbn}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    tanggal_kembali = datetime.now() + timedelta(days=14)
    new_peminjaman = {
        id_pinjam: {
            'nim': nim,
            'isbn': isbn,
            'tanggal_pinjam': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tanggal_kembali': tanggal_kembali.strftime('%Y-%m-%d'),
            'dikembalikan': False
        }
    }
    updated_peminjaman = {**state['peminjaman'], **new_peminjaman}
    updated_state = {**state, 'buku': updated_buku, 'peminjaman': updated_peminjaman}
    return updated_state, tanggal_kembali

def kembalikan_buku(state, nim, pilihan):
    pinjaman_pengguna = [
        (id_pinjam, pinjam) for id_pinjam, pinjam in state['peminjaman'].items()
        if pinjam['nim'] == nim and not pinjam['dikembalikan']
    ]
    if not pinjaman_pengguna or not (0 <= pilihan < len(pinjaman_pengguna)):
        return state, False
    
    id_pinjam, pinjam = pinjaman_pengguna[pilihan]
    updated_peminjaman = {**state['peminjaman'], id_pinjam: {**pinjam, 'dikembalikan': True}}
    updated_buku = {
        **state['buku'],
        pinjam['isbn']: {**state['buku'][pinjam['isbn']], 'jumlah': state['buku'][pinjam['isbn']]['jumlah'] + 1}
    }
    updated_state = {**state, 'peminjaman': updated_peminjaman, 'buku': updated_buku}
    return updated_state, True

def lihat_buku(state):
    return state['buku']

def lihat_peminjaman(state, nim):
    return [pinjam for pinjam in state['peminjaman'].values() if pinjam['nim'] == nim]

def lihat_semua_peminjaman(state):
    return state['peminjaman']

def lihat_profil(state, nim):
    return state['profil'].get(nim, {})

def lihat_teman(state, nim):
    return state['teman'].get(nim, [])

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
            nim = input("Masukkan NIM Anda (15 digit): ")
            password = input("Masukkan password: ")
            state, success = daftar(state, nim, password)
            if success:
                print("Pendaftaran berhasil!")
            else:
                print("Pendaftaran gagal: NIM sudah terdaftar atau NIM tidak valid.")
        
        elif pilihan == '2':
            nim = input("Masukkan NIM: ")
            password = input("Masukkan password: ")
            user_nim = masuk(state, nim, password)
            if user_nim:
                print("Berhasil masuk!")
                if state['profil'][user_nim]['role'] == 'admin':
                    while True:
                        print("\n=== Menu Admin ===")
                        print("1. Tambah Buku")
                        print("2. Lihat Buku")
                        print("3. Lihat Semua Peminjaman")
                        print("4. Keluar")
                        
                        pilihan_admin = input("Masukkan pilihan Anda: ")
                        
                        if pilihan_admin == '1':
                            isbn = input("Masukkan ISBN: ")
                            judul = input("Masukkan judul: ")
                            penulis = input("Masukkan penulis: ")
                            print("Kategori yang tersedia:")
                            for i, kategori in enumerate(KATEGORI, 1):
                                print(f"{i}. {kategori}")
                            pilihan_kategori = int(input("Pilih nomor kategori: ")) - 1
                            kategori = KATEGORI[pilihan_kategori] if 0 <= pilihan_kategori < len(KATEGORI) else 'Fiksi'
                            jumlah = int(input("Masukkan jumlah: "))
                            state, success = tambah_buku(state, isbn, judul, penulis, kategori, jumlah)
                            if success:
                                print("Buku berhasil ditambahkan!")
                            else:
                                print("Buku dengan ISBN ini sudah ada.")
                        elif pilihan_admin == '2':
                            buku = lihat_buku(state)
                            for isbn, info in buku.items():
                                print(f"ISBN: {isbn}, Judul: {info['judul']}, Penulis: {info['penulis']}, Jumlah: {info['jumlah']}")
                        elif pilihan_admin == '3':
                            peminjaman = lihat_semua_peminjaman(state)
                            for id_pinjam, pinjam in peminjaman.items():
                                status = 'Dikembalikan' if pinjam['dikembalikan'] else 'Belum dikembalikan'
                                print(f"ID: {id_pinjam}, NIM: {pinjam['nim']}, ISBN: {pinjam['isbn']}, Status: {status}")
                        elif pilihan_admin == '4':
                            print("Keluar dari akun admin...")
                            break
                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
                else:
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
                        
                        pilihan_user = input("Masukkan pilihan Anda: ")
                        
                        if pilihan_user == '1':
                            profil = lihat_profil(state, user_nim)
                            print(profil)
                        elif pilihan_user == '2':
                            nama = input("Masukkan nama: ")
                            email = input("Masukkan email: ")
                            state = isi_profil(state, user_nim, nama, email)
                            print("Profil berhasil diperbarui!")
                        elif pilihan_user == '3':
                            teman = lihat_teman(state, user_nim)
                            print(teman)
                        elif pilihan_user == '4':
                            nim_teman = input("Masukkan NIM teman: ")
                            state, success = tambah_teman(state, user_nim, nim_teman)
                            if success:
                                print(f"Teman dengan NIM {nim_teman} berhasil ditambahkan!")
                            else:
                                print(f"Tidak ada pengguna dengan NIM {nim_teman}.")
                        elif pilihan_user == '5':
                            teman_list = lihat_teman(state, user_nim)
                            for i, t in enumerate(teman_list):
                                print(f"{i + 1}. NIM: {t}")
                            pilihan = int(input("Masukkan nomor teman yang ingin dihapus: ")) - 1
                            state, success = hapus_teman(state, user_nim, pilihan)
                            if success:
                                print("Teman berhasil dihapus.")
                            else:
                                print("Pilihan tidak valid.")
                        elif pilihan_user == '6':
                            buku = lihat_buku(state)
                            for isbn, info in buku.items():
                                print(f"ISBN: {isbn}, Judul: {info['judul']}, Penulis: {info['penulis']}, Jumlah: {info['jumlah']}")
                        elif pilihan_user == '7':
                            isbn = input("Masukkan ISBN buku yang ingin dipinjam: ")
                            state, tanggal_kembali = pinjam_buku(state, user_nim, isbn)
                            if tanggal_kembali:
                                print(f"Buku berhasil dipinjam! Harap kembalikan sebelum {tanggal_kembali}.")
                            else:
                                print("Buku tidak ditemukan atau tidak tersedia.")
                        elif pilihan_user == '8':
                            pinjaman_pengguna = lihat_peminjaman(state, user_nim)
                            for i, pinjam in enumerate(pinjaman_pengguna):
                                print(f"{i + 1}. ISBN: {pinjam['isbn']}, Judul: {state['buku'][pinjam['isbn']]['judul']}")
                            pilihan = int(input("Masukkan nomor buku yang ingin dikembalikan: ")) - 1
                            state, success = kembalikan_buku(state, user_nim, pilihan)
                            if success:
                                print("Buku berhasil dikembalikan.")
                            else:
                                print("Pilihan tidak valid.")
                        elif pilihan_user == '9':
                            peminjaman = lihat_peminjaman(state, user_nim)
                            for pinjam in peminjaman:
                                status = 'Dikembalikan' if pinjam['dikembalikan'] else 'Belum dikembalikan'
                                print(f"Buku: {state['buku'][pinjam['isbn']]['judul']}, Status: {status}")
                        elif pilihan_user == '10':
                            print("Keluar dari akun...")
                            break
                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
        
        elif pilihan == '3':
            print("Terima kasih telah menggunakan Sistem Manajemen Perpustakaan. Sampai jumpa!")
            break

    simpan_data(state['pengguna'], FILE_PENGGUNA)
    simpan_data(state['profil'], FILE_PROFIL)
    simpan_data(state['teman'], FILE_TEMAN)
    simpan_data(state['buku'], FILE_BUKU)
    simpan_data(state['peminjaman'], FILE_PEMINJAMAN)

if __name__ == "__main__":
    main()
