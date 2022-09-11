from flask import Blueprint, render_template,url_for , redirect, jsonify, request, flash, session
from backend.auth import login_required
from backend.db import db, get_all_collection
from werkzeug.security import generate_password_hash

usersapp = Blueprint('usersapp', __name__)

# READ ALL
@usersapp.route('/users')
@login_required
def users():
    users_ref = db.collection('users').stream()
    users = []
    for user in users_ref:
        use = user.to_dict()
        use['id'] = user.id
        users.append(use) 
    
    return render_template('pengguna/users.html', users=users)

# CREATE
@usersapp.route('/users/tambah', methods=['POST','GET'])
@login_required
def tambah_users():
    if request.method == 'POST':
        # CEK KESAMAAN PASSWORD
        if request.form['password'] != request.form['password_1']:
            flash('Password Tidak Sama', 'danger')
            return redirect(url_for('.tambah_users'))
        
        # MEMANGGIL DATABASE
        cek_username = db.collection('users').where('username', '==', request.form['username']).stream()
        username = {}
        # PERULANGAN DATABSE
        for p in cek_username:
            user = p.to_dict()
            username = user
        # PENGECEKAN USERNAME
        if username:
            flash('Username Sudah Ada', 'danger')
            return redirect(url_for('.tambah_users'))
        
        data = {
        'nama_lengkap': request.form['nama_lengkap'],
        'username': request.form['username'],
        'email': request.form['email'],
        }
    
        data['password'] = generate_password_hash(request.form['password'], 'sha256')
        db.collection('users').document().set(data)
        flash('Berhasil Menambahkan User', 'success')
        return redirect(url_for('usersapp.users'))
    # sha256$bjjLvDNt$4881b16d1e48832a42a53604d73868b8b4e75c2b39e16be7949feb452500d2f1
        
    return render_template('pengguna/tambah_users.html')

# UPDATE
@usersapp.route('/users/edit/<uid>', methods=['POST','GET'])
@login_required
def edit_users(uid):
    if request.method == 'POST':
        user = {
            'nama_lengkap': request.form['nama_lengkap'],
            'email': request.form['email'],
            
        }
        
        session['user']['nama_lengkap'] = user['nama_lengkap']
        
        db.collection('users').document(uid).update(user)
        flash('Berhasil Update Data', 'success')
        return redirect(url_for('.users'))
        
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('pengguna/edit_users.html', data=data)

# DELETE
@usersapp.route('/users/hapus', methods=['POST'])
@login_required
def hapus_users():
    if request.method == 'POST':
        uid = request.form.get('uid')
        db.collection('users').document(uid).delete()
        flash('Berhasil Hapus Data', 'danger')
        return ('',204)
    # return "<h1 style='color: red'>Hello World</h1>"

# READ
@usersapp.route('/users/lihat/<uid>')
@login_required
def lihat_users(uid):
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('pengguna/lihat_users.html', data=data)