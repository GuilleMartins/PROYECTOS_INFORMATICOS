from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user

def admin_required(f):
    """
    Decorador para restringir el acceso exclusivamente a usuarios con rol ADMIN.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta sección.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('Acceso denegado: Se requieren privilegios de Administrador.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def tech_or_admin_required(f):
    """
    Decorador para permitir el acceso a Técnicos y Administradores.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta sección.', 'warning')
            return redirect(url_for('auth.login'))
        if not (current_user.is_admin() or current_user.is_technician()):
            flash('Acceso denegado: No posee los permisos técnicos requeridos.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
