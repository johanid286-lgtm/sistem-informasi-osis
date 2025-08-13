import os

target_db = "database.db"
project_dir = "."  # cari di folder saat ini

print(f"[INFO] Mencari koneksi ke '{target_db}'...\n")

found = False
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py") or file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if target_db in content:
                    print(f"[FOUND] {target_db} ditemukan di: {path}")
                    found = True
            except Exception as e:
                print(f"[SKIP] {path} (tidak bisa dibaca)")

if not found:
    print(f"[OK] Tidak ada file yang mengarah ke '{target_db}'")
