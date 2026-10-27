
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.modules.auth import auth_bp
from app.models.user import User


# INICIO DE SESIÓN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not username or not password:
            flash('Complete todos los campos obligatorios.', 'warning')
            return render_template('auth/login.html', username=username)

        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if not user or not user.check_password(password):
            flash('Credenciales incorrectas.', 'danger')
            return render_template('auth/login.html', username=username)

        if not user.is_active:
            flash('Su cuenta está desactivada.', 'danger')
            return render_template('auth/login.html', username=username)

        login_user(user, remember=remember)
        flash(f'¡Bienvenido/a, {user.first_name}!', 'success')

        next_page = request.args.get('next')
        if (
            next_page
            and next_page.startswith('/')
            and not next_page.startswith('//')
            and not next_page.startswith('/\\')
        ):
            return redirect(next_page)

        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')


# CIERRE DE SESIÓN
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Ha cerrado su sesión de forma segura.', 'info')
    return redirect(url_for('auth.login'))


