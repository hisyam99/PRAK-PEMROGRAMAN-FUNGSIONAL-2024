Perubahan yang dilakukan dari Modul 1 ke Modul 2 sekarang:

1. Penghapusan variabel global:
   - Sebelumnya, program menggunakan variabel global seperti `pengguna`, `profil`, `teman`, `buku`, dan `peminjaman`.
   - Sekarang, semua data tersebut disimpan dalam satu dictionary bernama `state`.
   - Ini membuat program lebih mudah dikelola dan menghindari efek samping yang tidak diinginkan.

2. Perubahan fungsi-fungsi utama:
   - Semua fungsi sekarang menerima `state` sebagai parameter dan mengembalikan `state` yang telah diperbarui.
   - Contoh: `def daftar(state):` alih-alih `def daftar():`.
   - Ini membuat fungsi-fungsi menjadi "murni" (pure functions), yang merupakan konsep penting dalam pemrograman fungsional.

3. Penghapusan efek samping:
   - Fungsi-fungsi tidak lagi langsung menyimpan data ke file atau mengubah variabel global.
   - Sebagai gantinya, mereka mengembalikan state yang diperbarui dan pesan.
   - Penyimpanan data ke file hanya dilakukan di akhir program dalam fungsi `main()`.

4. Perubahan pada fungsi `daftar()`:
   - Sekarang menggunakan fungsi helper `validate_nim()` dan `create_user_data()`.
   - Mengembalikan state yang diperbarui dan pesan, alih-alih langsung menyimpan data.

5. Perubahan pada fungsi `masuk()`:
   - Menggunakan fungsi helper `validate_login()`.
   - Mengembalikan NIM dan pesan, bukan mengubah variabel global.

6. Perubahan pada fungsi `isi_profil()`:
   - Menggunakan fungsi helper `update_profile()`.
   - Mengembalikan state yang diperbarui dan pesan.

7. Perubahan pada fungsi `tambah_teman()`:
   - Menggunakan fungsi helper `add_friend()`.
   - Mengembalikan state yang diperbarui dan pesan.

8. Perubahan pada fungsi-fungsi lain seperti `hapus_teman()`, `pinjam_buku()`, `kembalikan_buku()`:
   - Semua fungsi ini sekarang menerima `state` sebagai parameter.
   - Mereka mengembalikan state yang diperbarui dan pesan, alih-alih langsung mengubah data.

9. Penambahan fungsi `menu_pengguna()` dan `menu_admin()`:
   - Fungsi-fungsi ini sekarang mengelola state dan mengembalikannya.
   - Mereka memanggil fungsi-fungsi lain dan memperbarui state berdasarkan hasilnya.

10. Perubahan pada fungsi `main()`:
    - Sekarang menginisialisasi `state` di awal dengan memuat semua data dari file.
    - Mengelola state sepanjang jalannya program.
    - Menyimpan semua data ke file hanya di akhir program.

11. Penambahan struktur `if __name__ == "__main__":`:
    - Ini memastikan bahwa fungsi `main()` hanya dijalankan jika file dieksekusi langsung, bukan diimpor sebagai modul.

Secara keseluruhan, perubahan-perubahan ini membuat program Anda lebih sesuai dengan prinsip-prinsip pemrograman fungsional:

- Fungsi-fungsi menjadi lebih murni (pure) dan dapat diprediksi.
- Menghindari perubahan state secara langsung (mutasi).
- Mengurangi efek samping dengan memisahkan logika bisnis dari operasi I/O.
- Membuat alur data lebih jelas dengan selalu mengembalikan state yang diperbarui.

Pendekatan ini membuat program lebih mudah diuji, dipelihara, dan dipahami, karena setiap fungsi memiliki tanggung jawab yang jelas dan tidak bergantung pada variabel global atau efek samping yang tersembunyi.