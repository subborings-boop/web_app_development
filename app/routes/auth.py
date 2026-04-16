from flask import Blueprint, render_template, request, redirect, url_for, flash, session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊表單"""
    pass

@bp.route('/register', methods=['POST'])
def register():
    """接收註冊表單，建立帳號後重導向至登入頁"""
    pass

@bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入表單"""
    pass

@bp.route('/login', methods=['POST'])
def login():
    """處理登入邏輯，驗證帳密並設定 session"""
    pass

@bp.route('/logout', methods=['GET'])
def logout():
    """清除 session，登出並重導向首頁"""
    pass
