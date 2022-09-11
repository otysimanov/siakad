from flask import Blueprint, redirect, render_template, url_for, jsonify, flash, request, session
from werkzeug.security import check_password_hash
from backend.db import db, get_all_collection
from functools import wraps

auth = Blueprint('auth',__name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('auth.login'))
    return wrapper

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cek_username = db.collection('users').where('username', '==', username).stream()
        user = {}
        for ck in cek_username:
            user = ck.to_dict()
            user['id'] = ck.id
        
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user
                flash('Berhasil Login', 'success')
                return redirect(url_for('mahasiswa.daftar_mahasiswa'))
            else:
                flash('Password Anda Salah', 'danger')
                return redirect(url_for('.login'))
        else:
            flash('User Tidak Terdaftar', 'danger')
            return redirect(url_for('.login')) 
        
    if 'user' in session:
        flash('Anda Sudah Login', 'warning')
        return redirect(url_for('mahasiswa'))
    
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('Berhasil Logout', 'success')
    
    return redirect(url_for('.login'))
@auth.route('/coba')
def coba():
    return session['user']