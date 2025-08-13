import sqlite3

# Fungsi cek isi database.db
def cek_database():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM anggota").fetchall()
    conn.close()
    print("=== ISI database.db ===")
    for row in data:
        print(dict(row))

# Fungsi update manual untuk cek
def update_manual(id, nama, jabatan, angkatan):
    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE anggota SET nama=?, jabatan=?, angkatan=? WHERE id=?",
                 (nama, jabatan, angkatan, id))
    conn.commit()
    conn.close()
    print(f"[OK] Anggota id={id} berhasil diupdate di database.db")

if __name__ == "__main__":
    print("Sebelum update:")
    cek_database()

    # Ubah id=1 (sesuaikan dengan data kamu)
    update_manual(1, "Tes Nama", "Tes Jabatan", "2025")

    print("\nSesudah update:")
    cek_database()
