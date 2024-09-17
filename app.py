from flask import Flask
import os
from project.routes.routes import register_routes
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Gera uma chave secreta aleatória

@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('assets', filename)
# Registra as rotas a partir do arquivo routes.py
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
