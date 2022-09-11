from flask import Blueprint, redirect, render_template, url_for, jsonify, flash, request, session
from backend.db import db, get_all_collection, storage
from backend.auth import login, login_required

mahasiswa = Blueprint('mahasiswa', __name__)

@mahasiswa.route('/mahasiswa')
@login_required 
def daftar_mahasiswa():
    daftar_mahasiswa = get_all_collection('mahasiswa')
    return render_template('mahasiswa.html', mahasiswa=daftar_mahasiswa)

@mahasiswa.route('/mahasiswa/tambah', methods=['POST', 'GET'])
@login_required
def tambah_mahasiswa():
    if request.method == 'POST':
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'jurusan': request.form['jurusan'],
            'email': request.form['email'],
            'umur': request.form['umur'],
            
        }
        
        gambar = ['ktp', 'ktm', 'pas_foto']
        for gam in gambar:
            if gam in request.files and request.files[gam]:
                image = request.files[gam]
                ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
                filename = image.filename
                lokasi = f"mahasiswa/{filename}"
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ALLOWED_EXTENSIONS:
                    storage.child(lokasi).put(image)
                    data[gam] = storage.child(lokasi).get_url(None)
                else:
                    flash("Foto tidak diperbolehkan", "danger")
                    return redirect(url_for('.tambah_mahasiswa'))               

        db.collection('mahasiswa').document().set(data)
        flash('Berhasil Tambahkan Data Mahasiswa', 'success')
        return redirect(url_for('.daftar_mahasiswa'))
            
        
    return render_template('tambah_mahasiswa.html')