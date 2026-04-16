from flask import Blueprint, render_template
from app.models import Recipe, Ingredient

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """顯示首頁，包含搜尋入口與推薦/最新食譜列表"""
    try:
        # 取得最新公開食譜
        recipes = Recipe.get_all(public_only=True)
        # 取得所有可用食材供過濾搜尋用
        ingredients = Ingredient.get_all()
        return render_template('index.html', recipes=recipes, ingredients=ingredients)
    except Exception as e:
        print(f"Index Route Error: {e}")
        return render_template('index.html', recipes=[], ingredients=[])
