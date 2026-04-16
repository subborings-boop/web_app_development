from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """顯示首頁，包含搜尋入口與推薦/最新食譜列表"""
    pass
