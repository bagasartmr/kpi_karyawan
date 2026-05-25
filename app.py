from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# KONFIGURASI DATABASE
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_kpi_karyawan'

mysql = MySQL(app)


# =========================
# ROUTE DASHBOARD
# =========================

@app.route('/')
def index():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM karyawan")

    data = cur.fetchall()

    total = len(data)

    cur.close()

    return render_template(
        'index.html',
        karyawan=data,
        total=total
    )

# =========================
# ROUTE TAMBAH DATA KARYAWAN
# =========================

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():

    if request.method == 'POST':

        nama = request.form['nama']
        jabatan = request.form['jabatan']
        divisi = request.form['divisi']
        alamat = request.form['alamat']
        no_hp = request.form['no_hp']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO karyawan
            (nama, jabatan, divisi, alamat, no_hp)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama, jabatan, divisi, alamat, no_hp))

        mysql.connection.commit()

        cur.close()

        return redirect('/')

    return render_template('tambah.html')

# =========================
# ROUTE HAPUS DATA KARYAWAN
# =========================

@app.route('/hapus/<int:id>')
def hapus(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM karyawan WHERE id_karyawan=%s", (id,))

    mysql.connection.commit()

    cur.close()

    return redirect('/')

# =========================
# ROUTE EDIT DATA KARYAWAN
# =========================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        nama = request.form['nama']
        jabatan = request.form['jabatan']
        divisi = request.form['divisi']
        alamat = request.form['alamat']
        no_hp = request.form['no_hp']

        cur.execute("""
            UPDATE karyawan
            SET
                nama=%s,
                jabatan=%s,
                divisi=%s,
                alamat=%s,
                no_hp=%s
            WHERE id_karyawan=%s
        """, (nama, jabatan, divisi, alamat, no_hp, id))

        mysql.connection.commit()

        cur.close()

        return redirect('/')

    cur.execute("SELECT * FROM karyawan WHERE id_karyawan=%s", (id,))

    data = cur.fetchone()

    cur.close()

    return render_template('edit.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

