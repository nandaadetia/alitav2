import os
import json
import sys
import subprocess

def warna(teks, kode):
    #Mengembalikan teks berwarna untuk output terminal.
    return f"\033[{kode}m{teks}\033[0m"

def periksa_pembaruan():
    #Memeriksa pembaruan di repository GitHub dan menarik perubahan jika ada.
    repo_url = "https://github.com/nandaadetia/alitav2.git"
    repo_path = os.path.dirname(os.path.abspath(__file__))
    
    try:
        if not os.path.exists(os.path.join(repo_path, ".git")):
            print(warna("[INFO] Repository belum dikloning, mengkloning sekarang...", 34))
            subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        else:
            print(warna("[INFO] Memeriksa pembaruan...", 34))
            subprocess.run(["git", "pull"], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(warna(f"[ERROR] Gagal memperbarui repository: {e}", 31))

def baca_database(nama_file):
    #Membaca database JSON dan mengembalikan data.
    if not os.path.exists(nama_file):
        print(warna(f"[WARNING] Database '{nama_file}' tidak ditemukan.", 33))
        return []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(warna(f"[ERROR] Gagal membaca '{nama_file}', format JSON tidak valid.", 31))
        return []

def cari_kata(database, awalan, kata_terlarang, max_result=10, urut_panjang=False):
    #Mencari kata berdasarkan awalan, menghindari kata terlarang.
    hasil = [kata for kata in database if kata.startswith(awalan.lower()) and kata not in kata_terlarang]
    if urut_panjang:
        hasil.sort(key=len, reverse=True)
    else:
        hasil.sort()
    return hasil[:max_result]

def tampilkan_hasil(nama_db, hasil, ada_hasil):
    #Menampilkan hasil pencarian dengan format yang lebih rapi dan berwarna.
    if hasil:
        print(f"\n>> Hasil dari {nama_db}:")
        print(warna("   " + " | ".join(hasil), 32))
        return True
    return ada_hasil

def main():
    periksa_pembaruan()
    
    nama_files = {
        "KBBI": "newkbbifix.json",
        "SEMI COUNTER": "katafix.json",
        "NOCOUNTER": "nocounter.json",
        "KATA PANJANG": "katapanjang.json",

    }
    
    databases = {nama: baca_database(file) for nama, file in nama_files.items()}
    kata_terlarang = {"allah"}
    
    if all(not db for db in databases.values()):
        print(warna("[ERROR] Tidak ada database yang tersedia. Program dihentikan.", 31))
        return
    
    if len(sys.argv) > 1:
        awalan = sys.argv[1]
        ada_hasil = False
        for nama, db in databases.items():
            urut_panjang = nama == "KATA PANJANG"
            hasil = cari_kata(db, awalan, kata_terlarang, urut_panjang=urut_panjang)
            ada_hasil = tampilkan_hasil(nama, hasil, ada_hasil)
        if not ada_hasil:
            print(warna("\n[INFO] Tidak ada hasil dalam semua database.", 31))
        return
    
    while True:
        awalan = input("\nMasukkan awalan kata (Enter untuk keluar): ").strip()
        if not awalan:
            print(warna("\n[INFO] Program selesai.", 34))
            break
        
        ada_hasil = False
        for nama, db in databases.items():
            urut_panjang = nama == "KATA PANJANG"
            hasil = cari_kata(db, awalan, kata_terlarang, urut_panjang=urut_panjang)
            ada_hasil = tampilkan_hasil(nama, hasil, ada_hasil)
        if not ada_hasil:
            print(warna("\n[INFO] Tidak ada hasil dalam semua database.", 31))

if __name__ == "__main__":
    main()
