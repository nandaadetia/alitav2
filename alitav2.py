import os
import json
import sys

def warna(teks, kode):
    """Mengembalikan teks berwarna untuk output terminal."""
    return f"\033[{kode}m{teks}\033[0m"

def baca_database(nama_file):
    """Membaca database JSON dan mengembalikan data."""
    if not os.path.exists(nama_file):
        print(warna(f"[WARNING] Database '{nama_file}' tidak ditemukan.", 33))
        return []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(warna(f"[ERROR] Gagal membaca '{nama_file}', format JSON tidak valid.", 31))
        return []

def cari_kata(database, awalan, kata_terlarang, max_result=10):
    """Mencari kata berdasarkan awalan, menghindari kata terlarang."""
    return [kata for kata in database if kata.startswith(awalan.lower()) and kata not in kata_terlarang][:max_result]

def tampilkan_hasil(nama_db, hasil):
    """Menampilkan hasil pencarian dengan format yang lebih rapi dan berwarna."""
    print(f"\n>> Hasil dari {nama_db}:")
    if hasil:
        print(warna("   " + " | ".join(hasil), 32))  # Hijau untuk hasil ditemukan
    else:
        print(warna("   [Tidak ada hasil]", 31))  # Merah untuk hasil kosong

def main():
    """Fungsi utama program."""
    nama_files = {
        "KBBI": "newkbbifix.json",
        "KATA KERAMAT": "katafix.json",
        "KATA PANJANG": "katapanjang.json",
    }
    
    databases = {nama: baca_database(file) for nama, file in nama_files.items()}
    kata_terlarang = {"angel", "allah", "esa", "tuhan", "zion", "yesus"}
    
    if all(not db for db in databases.values()):
        print(warna("[ERROR] Tidak ada database yang tersedia. Program dihentikan.", 31))
        return
    
    # Mode CLI
    if len(sys.argv) > 1:
        awalan = sys.argv[1]
        for nama, db in databases.items():
            hasil = cari_kata(db, awalan, kata_terlarang)
            tampilkan_hasil(nama, hasil)
        return
    
    # Mode interaktif
    while True:
        awalan = input("\nMasukkan awalan kata (Enter untuk keluar): ").strip()
        if not awalan:
            print(warna("\n[INFO] Program selesai.", 34))  # Biru untuk info
            break
        
        for nama, db in databases.items():
            hasil = cari_kata(db, awalan, kata_terlarang)
            tampilkan_hasil(nama, hasil)

if __name__ == "__main__":
    main()
