
from flask import render_template, request, redirect, session, flash, url_for
import json
from flask_app import app
from flask_app.controllers import users

if __name__ == "__main__":
    app.run(debug=True)
