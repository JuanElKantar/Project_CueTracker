from flask import Flask, render_template, session
from flask_session import Session
from partida import partida_bp
from login import login_bp
from registrar import registrar_bp
from config import config_bp
from admin import admin_bp
from user import user_bp
from reportes import reportes_bp  
from mesas import mesas_bp
from estadisticas import estadisticas_bp

app = Flask(__name__)
app.debug = True
app.secret_key = 'your_secret_key_here'

app.config['SESSION_TYPE'] = 'filesystem'  # Puedes ajustar el tipo de almacenamiento según tus necesidades
Session(app)

app.register_blueprint(partida_bp)
app.register_blueprint(login_bp)
app.register_blueprint(registrar_bp)
app.register_blueprint(config_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(reportes_bp)  
app.register_blueprint(mesas_bp)
app.register_blueprint(estadisticas_bp)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run()
