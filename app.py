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

    cur.execute("""

        SELECT

            k.id_karyawan,
            k.nama,
            k.jabatan,
            k.divisi,
            k.alamat,
            k.no_hp,

            p.kualitas,
            p.kuantitas,
            p.kehadiran,
            p.disiplin,
            p.total_kpi,
            p.grade

        FROM karyawan k

        LEFT JOIN penilaian_kpi p
        ON p.id_penilaian = (

            SELECT MAX(id_penilaian)

            FROM penilaian_kpi

            WHERE id_karyawan = k.id_karyawan

        )

    """)

    data = cur.fetchall()

    total = len(data)

    cur.close()

    return render_template(
        'index.html',
        data=data,
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

# =========================
# ROUTE INPUT KPI KARYAWAN
# =========================

@app.route('/kpi', methods=['GET', 'POST'])
def kpi():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM karyawan")

    karyawan = cur.fetchall()

    if request.method == 'POST':

        id_karyawan = request.form['id_karyawan']

        kualitas = int(request.form['kualitas'])
        kuantitas = int(request.form['kuantitas'])

        absensi = int(request.form['absensi'])
        pulang_cepat = int(request.form['pulang_cepat'])

        sanksi = int(request.form['sanksi'])
        ketepatan_hadir = int(request.form['ketepatan_hadir'])

        # Rata-rata Kehadiran
        kehadiran = (absensi + pulang_cepat) / 2

        # Rata-rata Disiplin
        disiplin = (sanksi + ketepatan_hadir) / 2

        # Total KPI
        total_kpi = kualitas + kuantitas + kehadiran + disiplin

        # Grade
        if total_kpi >= 19:
            grade = 'BS'

        elif total_kpi >= 16:
            grade = 'B'

        elif total_kpi >= 12:
            grade = 'S'

        elif total_kpi >= 8:
            grade = 'C'

        else:
            grade = 'K'

        cur.execute("""
            INSERT INTO penilaian_kpi (

                id_karyawan,
                kualitas,
                kuantitas,
                absensi,
                pulang_cepat,
                sanksi,
                ketepatan_hadir,
                kehadiran,
                disiplin,
                total_kpi,
                grade

            )

            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """, (

            id_karyawan,
            kualitas,
            kuantitas,
            absensi,
            pulang_cepat,
            sanksi,
            ketepatan_hadir,
            kehadiran,
            disiplin,
            total_kpi,
            grade

        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/')

    return render_template('kpi.html', karyawan=karyawan)

if __name__ == '__main__':
    app.run(debug=True)

