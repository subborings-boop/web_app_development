from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models import Recipe, Ingredient
from .auth import login_required

bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@bp.route('/', methods=['GET'])
def list_recipes():
    """顯示食譜列表，若帶有 ?q= 參數則執行關鍵字搜尋"""
    q = request.args.get('q', '').strip()
    try:
        all_recipes = Recipe.get_all(public_only=True)
        if q:
            recipes = [r for r in all_recipes if q.lower() in r.title.lower() or (r.description and q.lower() in r.description.lower())]
        else:
            recipes = all_recipes
        return render_template('recipe/list.html', recipes=recipes, query=q)
    except Exception as e:
        flash(f"讀取失敗：{e}", "danger")
        return redirect(url_for('main.index'))

@bp.route('/search_by_ingredients', methods=['GET'])
def search_by_ingredients():
    """接收 ingredients 陣列參數，回傳符合的食譜列表"""
    try:
        ingredients = Ingredient.get_all()
        selected_ing_ids = request.args.getlist('ing', type=int)
        
        recipes = []
        if selected_ing_ids:
            recipes = Recipe.search_by_ingredients(selected_ing_ids)
            
        return render_template('recipe/search_result.html', recipes=recipes, ingredients=ingredients, selected_ids=selected_ing_ids)
    except Exception as e:
        flash(f"搜尋發生錯誤：{e}", "danger")
        return redirect(url_for('main.index'))

@bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """顯示單筆食譜詳情"""
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if not recipe:
            abort(404)
        if not recipe.is_public and recipe.user_id != session.get('user_id'):
            flash("這是一篇私密食譜，僅作者可以查看。", "warning")
            return redirect(url_for('main.index'))
            
        recipe.ingredients = Recipe.get_ingredients(recipe_id)
        return render_template('recipe/detail.html', recipe=recipe)
    except Exception as e:
        flash(f"讀取失敗：{e}", "danger")
        return redirect(url_for('main.index'))

@bp.route('/new', methods=['GET'])
@login_required
def new_page():
    """顯示新增食譜表單"""
    ingredients = Ingredient.get_all()
    return render_template('recipe/form.html', recipe=None, ingredients=ingredients, selected_ing_ids=[])

@bp.route('/', methods=['POST'])
@login_required
def create():
    """接收表單，新建食譜與食材關聯，儲存後重導向"""
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        is_public = 1 if request.form.get('is_public') == '1' else 0
        
        ingredient_ids = request.form.getlist('ingredients')
        ingredients_data = [(int(ing_id), "") for ing_id in ingredient_ids if ing_id]
        
        if not title or not steps:
            flash("食譜名稱與步驟為必填項目", "danger")
            return redirect(url_for('recipe.new_page'))
            
        recipe_id = Recipe.create({
            'user_id': session['user_id'],
            'title': title,
            'description': description,
            'steps': steps,
            'is_public': is_public,
            'ingredients_data': ingredients_data
        })
        flash("食譜新增成功！", "success")
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))
    except Exception as e:
        flash(f"新增失敗：{e}", "danger")
        return redirect(url_for('recipe.new_page'))

@bp.route('/<int:recipe_id>/edit', methods=['GET'])
@login_required
def edit_page(recipe_id):
    """顯示編輯表單，帶入舊資料"""
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if not recipe:
            abort(404)
        if recipe.user_id != session.get('user_id'):
            flash("您沒有權限編輯此篇食譜", "danger")
            return redirect(url_for('recipe.detail', recipe_id=recipe_id))
            
        recipe.ingredients = Recipe.get_ingredients(recipe_id)
        selected_ing_ids = [ing['id'] for ing in recipe.ingredients]
        all_ingredients = Ingredient.get_all()
        
        return render_template('recipe/form.html', recipe=recipe, ingredients=all_ingredients, selected_ing_ids=selected_ing_ids)
    except Exception as e:
        flash(f"讀取錯誤：{e}", "danger")
        return redirect(url_for('main.index'))

@bp.route('/<int:recipe_id>/update', methods=['POST'])
@login_required
def update(recipe_id):
    """接收表單，更新食譜與關聯食材"""
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if not recipe or recipe.user_id != session.get('user_id'):
            abort(403)
            
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        is_public = 1 if request.form.get('is_public') == '1' else 0
        
        ingredient_ids = request.form.getlist('ingredients')
        ingredients_data = [(int(ing_id), "") for ing_id in ingredient_ids if ing_id]
        
        Recipe.update(recipe_id, {
            'title': title,
            'description': description,
            'steps': steps,
            'is_public': is_public,
            'ingredients_data': ingredients_data
        })
        flash("食譜更新成功！", "success")
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))
    except Exception as e:
        flash(f"更新失敗：{e}", "danger")
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))

@bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete(recipe_id):
    """刪除指定食譜"""
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if not recipe or recipe.user_id != session.get('user_id'):
            abort(403)
            
        Recipe.delete(recipe_id)
        flash("食譜已成功刪除。", "info")
        return redirect(url_for('recipe.list_recipes'))
    except Exception as e:
        flash(f"刪除失敗：{e}", "danger")
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))
