import subprocess
from colorama import init, Fore

# Inisialisasi colorama
init()

def run_file(file_path):
    try:
        subprocess.check_call(['python', file_path])
        print(f"{Fore.GREEN}Berhasil menjalankan file {file_path}{Fore.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"Gagal menjalankan file {file_path}: {e}")

1
print("Pilih salah satu opsi:")
print("1. Scrab Gambar")
print("2. Download Gambar Di Postingan")

file_choice = input("Masukkan nomor pilihan: ")


if file_choice == '1':
    file_path = 'reamz.py'
    run_file(file_path)
elif file_choice == '2':
    file_path = 'reamz2.py'
    run_file(file_path)
else:
    print("Pilihan tidak valid.")
