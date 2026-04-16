import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊表單"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')

@bp.route('/register', methods=['POST'])
def register():
    """接收註冊表單，建立帳號後重導向至登入頁"""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    error = None

    if not username:
        error = '使用者名稱為必填欄位。'
    elif not email:
        error = '信箱為必填欄位。'
    elif not password:
        error = '密碼為必填欄位。'
    elif password != confirm_password:
        error = '兩次輸入的密碼不相符。'
    elif User.get_by_email(email) is not None:
        error = f"信箱 {email} 已經被註冊過了。"

    if error is None:
        try:
            # 密碼利用 bcrypt 轉換為雜湊字串
            hashed_pwd = generate_password_hash(password)
            User.create({
                'username': username,
                'email': email,
                'password_hash': hashed_pwd,
                'is_admin': 0
            })
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login_page'))
        except Exception as e:
            error = "註冊時發生錯誤，請稍後再試。"
            print(e)

    flash(error, 'danger')
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入表單"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def login():
    """處理登入邏輯，驗證帳密並設定 session"""
    email = request.form.get('email')
    password = request.form.get('password')
    error = None

    if not email or not password:
        error = '請輸入完整的信箱與密碼。'
    else:
        user = User.get_by_email(email)
        if user is None:
            error = '找不到此使用者。'
        elif not check_password_hash(user.password_hash, password):
            error = '密碼錯誤。'

    if error is None:
        session.clear()
        session['user_id'] = user.id
        session['username'] = user.username
        flash('登入成功！', 'success')
        return redirect(url_for('main.index'))

    flash(error, 'danger')
    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET'])
def logout():
    """清除 session，登出並重導向首頁"""
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))

def login_required(view):
    """
    自訂裝飾器，可加在其他需要登入才能訪問的路由上。
    若未登入會自動導向登入頁面。
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('請先登入後再進行此操作。', 'warning')
            return redirect(url_for('auth.login_page'))
        return view(**kwargs)
    return wrapped_view
