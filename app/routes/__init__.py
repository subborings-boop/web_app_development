from .auth import bp as auth_bp
from .recipe import bp as recipe_bp
from .main import bp as main_bp

__all__ = ['auth_bp', 'recipe_bp', 'main_bp']
