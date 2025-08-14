from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "osis123"

# Fungsi koneksi database
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # supaya bisa akses pakai nama kolom
    cur = conn.cursor()
    return cur, conn

# ------------------ HALAMAN UTAMA ------------------
@app.route('/home')
def index():

    if "username" not in session:
        return redirect(url_for("login"))

    cur, conn = get_db()
    cur.execute("SELECT * FROM kegiatan")
    kegiatan_list = cur.fetchall()
    conn.close()
    return render_template("index.html", kegiatan=kegiatan_list)

# ------------------ LOGIN ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Cek username & password (contoh statis)
        if username == "johan" and password == "123":
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Username atau password salah")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ------------------ CRUD KEGIATAN ------------------
@app.route("/kegiatan")
def kegiatan():
    cur, conn = get_db()
    cur.execute("SELECT * FROM kegiatan")
    data = cur.fetchall()
    conn.close() 
    return render_template('kegiatan.html', kegiatan=data)

@app.route("/manajemen_kegiatan")
def manajemen_kegiatan():
    # Ambil data kegiatan dari database
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM kegiatan")
    kegiatan_list = cur.fetchall()
    print([dict(k) for k in kegiatan_list])
    conn.close()
    return render_template('manajemen_kegiatan.html', kegiatan=kegiatan_list, enumerate=enumerate)

@app.route("/tambah_kegiatan", methods=["GET", "POST"])
def tambah_kegiatan():
    if request.method == "POST":
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        tanggal = request.form['tanggal']
        cur, conn = get_db()
        cur.execute("INSERT INTO kegiatan (nama, tanggal, deskripsi) VALUES (?, ?, ?)",
                    (nama, tanggal, deskripsi))
        conn.commit()
        conn.close()
        return redirect(url_for("kegiatan"))
    return render_template("tambah_kegiatan.html")

@app.route("/edit_kegiatan/<int:id>", methods=["GET", "POST"])
def edit_kegiatan(id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        nama = request.form["nama"]
        tanggal = request.form["tanggal"]
        deskripsi = request.form["deskripsi"]

        cur.execute("UPDATE kegiatan SET nama=?, tanggal=?, deskripsi=? WHERE id=?",
                     (nama, tanggal, deskripsi, id))
        conn.commit()
        conn.close()
        return redirect(url_for("manajemen_kegiatan"))

    keg = cur.execute("SELECT * FROM kegiatan WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_kegiatan.html", kegiatan=keg)

@app.route('/hapus_kegiatan/<int:id>', methods=['GET', 'POST'])
def hapus_kegiatan(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM kegiatan WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manajemen_kegiatan'))

@app.route("/presensi/<int:kegiatan_id>")
def tampil_presensi(kegiatan_id):
    cur, conn = get_db()  # pakai get_db() agar row_factory aktif

    # Ambil presensi beserta nama anggota dan nama kegiatan
    cur.execute("""
        SELECT p.id, k.nama AS nama_kegiatan, a.nama AS nama_anggota, p.status, p.tanggal
        FROM presensi p
        JOIN anggota a ON p.anggota_id = a.id
        JOIN kegiatan k ON p.kegiatan_id = k.id
        WHERE p.kegiatan_id = ?
        ORDER BY p.tanggal DESC
    """, (kegiatan_id,))
    
    presensi_list = cur.fetchall()
    conn.close()

    return render_template("presensi.html", presensi_list=presensi_list)

# ---------------- Presensi ----------------
@app.route("/tambah_presensi", methods=["GET", "POST"])
def tambah_presensi():
    cur, conn = get_db()
    cur.execute("SELECT * FROM kegiatan")
    kegiatan_list = cur.fetchall()
    cur.execute("SELECT * FROM anggota")
    anggota_list = cur.fetchall()
    if request.method == "POST":
        kegiatan_id = request.form['kegiatan_id']
        anggota_id = request.form['anggota_id']
        status = request.form['status']
        tanggal = request.form['tanggal']
        cur.execute("INSERT INTO presensi (kegiatan_id, anggota_id, status, tanggal) VALUES (?, ?, ?, ?)",
                    (kegiatan_id, anggota_id, status, tanggal))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("tambah_presensi.html", kegiatan_list=kegiatan_list, anggota_list=anggota_list)

# ------------------ CRUD ANGGOTA ------------------
@app.route("/anggota")
def anggota():
    cur, conn = get_db()
    cur.execute("SELECT * FROM anggota")
    anggota = cur.fetchall()
    conn.close()
    return render_template("daftar_anggota.html", anggota=anggota)


@app.route("/tambah_anggota", methods=["GET", "POST"])
def tambah_anggota():
    if request.method == "POST":
        nama = request.form.get("nama")
        kelas = request.form.get("kelas")
        jabatan = request.form.get("jabatan")
        angkatan = request.form.get("angkatan")

        cur, conn = get_db()
        cur.execute("""
            INSERT INTO anggota (nama, kelas, jabatan, angkatan)
            VALUES (?, ?, ?, ?)
        """, (nama, kelas, jabatan, angkatan))
        conn.commit()
        conn.close()

        return redirect(url_for("anggota"))

    return render_template("tambah_anggota.html")

@app.route('/hapus_anggota/<int:id>', methods=['POST'])
def hapus_anggota(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM anggota WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('anggota'))

@app.route("/presensi")
def tampil_semua_presensi():
    cur, conn = get_db()
    cur.execute("""
        SELECT p.id, k.nama AS nama_kegiatan, a.nama AS nama_anggota, p.status, p.tanggal
        FROM presensi p
        JOIN kegiatan k ON p.kegiatan_id = k.id
        JOIN anggota a ON p.anggota_id = a.id
        ORDER BY p.tanggal DESC
    """)
    presensi_list = cur.fetchall()
    conn.close()
    return render_template("presensi.html", presensi_list=presensi_list)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True,port=5035)
