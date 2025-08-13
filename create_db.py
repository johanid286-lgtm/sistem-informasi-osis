import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Tabel kegiatan
cursor.execute("""
CREATE TABLE IF NOT EXISTS kegiatan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    tanggal TEXT NOT NULL,
    deskripsi TEXT
)
""")

# Tabel anggota
cursor.execute("""
CREATE TABLE IF NOT EXISTS anggota (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    jabatan TEXT NOT NULL,
    angkatan TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Database berhasil dibuat!")
