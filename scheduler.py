import os
from ftplib import FTP
import datetime

# Konfigurasi FTP
ftp = FTP('ftp.example.com')
ftp.login(user='username', passwd='password')

# Konfigurasi tanggal
tanggal = datetime.date.today().strftime("%Y%m%d")

# Mendapatkan daftar folder di FTP
folders = ftp.nlst()

# Memindahkan file dari setiap folder ke server
for folder in folders:
    if folder.startswith(tanggal):
        # Masuk ke folder yang sesuai
        ftp.cwd(folder)

        # Mendapatkan daftar file di folder
        files = ftp.nlst()

        # Memindahkan setiap file ke server
        for file in files:
            if file.endswith('.csv'):
                # Membuat nama file yang baru
                new_filename = f"{tanggal}_{file}"

                # Menyalin file ke server
                with open(new_filename, 'wb') as f:
                    ftp.retrbinary('RETR ' + file, f.write)

                # Memindahkan file ke folder tujuan
                destination_folder = '/path/to/landing/server/folder'
                os.system(f"cp {new_filename} {destination_folder}")

                # Menghapus file sementara
                os.remove(new_filename)

        # Keluar dari folder
        ftp.cwd("..")

# Menutup koneksi FTP
ftp.quit()
