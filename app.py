from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "osis123"

# Fungsi koneksi database
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ HALAMAN UTAMA ------------------
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kegiatan ORDER BY tanggal DESC")
    kegiatan_list = cursor.fetchall()
    conn.close()
    return render_template("index.html", kegiatan=kegiatan_list)

# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "johan" and password == "1234":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Login gagal!")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ------------------ CRUD KEGIATAN ------------------
@app.route("/kegiatan")
def kegiatan():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM kegiatan")
    data = c.fetchall()
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

@app.route('/tambah_kegiatan', methods=['GET', 'POST'])
def tambah_kegiatan():
    if request.method == 'POST':
        nama = request.form['nama']
        tanggal = request.form['tanggal']
        deskripsi = request.form['deskripsi']

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO kegiatan (nama, tanggal, deskripsi) VALUES (?, ?, ?)",
                  (nama, tanggal, deskripsi))
        conn.commit()
        conn.close()

        return redirect(url_for('manajemen_kegiatan'))

    return render_template('tambah_kegiatan.html')


@app.route("/edit_kegiatan/<int:id>", methods=["GET", "POST"])
def edit_kegiatan(id):
    conn = get_db()
    if request.method == "POST":
        nama = request.form["nama"]
        tanggal = request.form["tanggal"]
        deskripsi = request.form["deskripsi"]

        conn.execute("UPDATE kegiatan SET nama=?, tanggal=?, deskripsi=? WHERE id=?",
                     (nama, tanggal, deskripsi, id))
        conn.commit()
        conn.close()
        return redirect(url_for("kegiatan"))

    keg = conn.execute("SELECT * FROM kegiatan WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_kegiatan.html", keg=keg)

@app.route('/hapus_kegiatan/<int:id>', methods=['POST'])
def hapus_kegiatan(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM kegiatan WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manajemen_kegiatan'))

# ------------------ CRUD ANGGOTA ------------------
@app.route("/anggota")
def anggota():
    conn = get_db()
    anggota_list = conn.execute("SELECT * FROM anggota").fetchall()
    conn.close()
    return render_template("anggota.html", anggota_list=anggota_list)

@app.route("/tambah_anggota", methods=["GET", "POST"])
def tambah_anggota():
    if request.method == "POST":
        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        angkatan = request.form["angkatan"]

        conn = get_db()
        conn.execute("INSERT INTO anggota (nama, jabatan, angkatan) VALUES (?, ?, ?)",
                     (nama, jabatan, angkatan))
        conn.commit()
        conn.close()
        return redirect(url_for("anggota"))
    return render_template("tambah_anggota.html")

@app.route("/edit_anggota/<int:id>", methods=["GET", "POST"])
def edit_anggota(id):
    conn = get_db()
    if request.method == "POST":
        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        angkatan = request.form["angkatan"]

        conn.execute("UPDATE anggota SET nama=?, jabatan=?, angkatan=? WHERE id=?",
                     (nama, jabatan, angkatan, id))
        conn.commit()
        conn.close()
        return redirect(url_for("anggota"))

    agt = conn.execute("SELECT * FROM anggota WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_anggota.html", agt=agt)


@app.route("/hapus_anggota/<int:id>")
def hapus_anggota(id):
    conn = get_db()
    conn.execute("DELETE FROM anggota WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("anggota"))

if __name__ == "__main__":
    app.run(debug=True,port=5019)
