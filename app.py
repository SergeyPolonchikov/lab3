from __future__ import annotations

import os
from dataclasses import dataclass

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)


@dataclass(frozen=True)
class User(UserMixin):
    id: str
    username: str
    password: str


DEMO_USER = User(id="1", username="user", password="qwerty")


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = (
        "Для доступа к запрашиваемой странице необходимо пройти аутентификацию."
    )
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id: str):
        if user_id == DEMO_USER.id:
            return DEMO_USER
        return None

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            remember = request.form.get("remember") == "on"

            if username == DEMO_USER.username and password == DEMO_USER.password:
                login_user(DEMO_USER, remember=remember)
                flash("Успешный вход.", "success")

                next_url = request.args.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect(url_for("index"))

            flash("Неверно введены логин или пароль.", "danger")

        return render_template("login.html")

    @app.get("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Вы вышли из системы.", "info")
        return redirect(url_for("index"))

    @app.get("/counter")
    def counter():
        session["counter_visits"] = int(session.get("counter_visits", 0)) + 1
        return render_template("counter.html", visits=session["counter_visits"])

    @app.get("/secret")
    @login_required
    def secret():
        return render_template("secret.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

