import os
import sys
import subprocess

def cek_dan_install(library, versi_diperlukan):
    try:
        # Cek apakah library sudah terinstall dan ambil versinya
        hasil = subprocess.check_output([sys.executable, '-m', 'pip', 'show', library])
        hasil = hasil.decode('utf-8').split('\n')
        versi_terinstall = None
        for baris in hasil:
            if baris.startswith('Version:'):
                versi_terinstall = baris.split()[1]
                break
        
        if versi_terinstall:
            print(f"{library} versi {versi_terinstall} sudah terinstall.")
            if versi_terinstall < versi_diperlukan:
                print(f"Versi {versi_terinstall} lebih rendah dari versi yang diperlukan {versi_diperlukan}. Menginstal versi terbaru...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', f'{library}=={versi_diperlukan}'])
            else:
                print(f"Versi {versi_terinstall} lebih tinggi atau sama dengan versi yang diperlukan {versi_diperlukan}.")
        else:
            raise subprocess.CalledProcessError(1, 'pip show')
    except subprocess.CalledProcessError:
        # Jika library belum terinstall, install library tersebut
        print(f"{library} belum terinstall. Menginstal {library}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', f'{library}=={versi_diperlukan}'])
        except subprocess.CalledProcessError as e:
            print(f"Gagal menginstal {library}: {e}")
            sys.exit(1)

# Baca file requirements.txt
with open('requirements.txt', 'r') as file:
    libraries = file.readlines()

# Cek dan install setiap library
for library in libraries:
    nama_library, versi_diperlukan = library.strip().split('==')
    cek_dan_install(nama_library, versi_diperlukan)

# Jalankan program Python
print("Menjalankan program Python...")
os.system('streamlit run dashboard.py')
