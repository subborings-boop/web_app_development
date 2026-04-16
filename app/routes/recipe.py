from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@bp.route('/', methods=['GET'])
def list_recipes():
    """顯示食譜列表，若帶有 ?q= 參數則執行關鍵字搜尋"""
    pass

@bp.route('/search_by_ingredients', methods=['GET'])
def search_by_ingredients():
    """接收 ingredients 陣列參數，回傳符合的食譜列表"""
    pass

@bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """顯示單筆食譜詳情"""
    pass

@bp.route('/new', methods=['GET'])
def new_page():
    """顯示新增食譜表單（需登入）"""
    pass

@bp.route('/', methods=['POST'])
def create():
    """接收表單，新建食譜與食材關聯，儲存後重導向（需登入）"""
    pass

@bp.route('/<int:recipe_id>/edit', methods=['GET'])
def edit_page(recipe_id):
    """顯示編輯表單，帶入舊資料（需為擁有者）"""
    pass

@bp.route('/<int:recipe_id>/update', methods=['POST'])
def update(recipe_id):
    """接收表單，更新食譜與關聯食材（需為擁有者）"""
    pass

@bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete(recipe_id):
    """刪除指定食譜（需為擁有者或管理員）"""
    pass
