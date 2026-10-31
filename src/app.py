import os
from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

# Lectura de variables de entorno configuradas en docker-compose
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "holamundo_db")

def check_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return True, f"Version de MySQL: {db_version}"
    except Exception as e:
        return False, str(e)

@app.route("/")
def index():
    success, message = check_db_connection()

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Hola Mundo Docker Compose</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: #eef2f7; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                margin: 0; 
            }
            .card { 
                background: white; 
                padding: 30px; 
                border-radius: 12px; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.1); 
                text-align: center; 
                max-width: 500px; 
                width: 100%; 
            }
            h1 { color: #1e3a8a; margin-bottom: 10px; }
            .badge { display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: bold; margin-top: 15px; }
            .success { background: #dcfce7; color: #15803d; }
            .error { background: #fee2e2; color: #b91c1c; }
            p.info { color: #64748b; font-size: 14px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Hola Mundo!</h1>
            <p>Aplicacion Web funcionando con <strong>Docker Compose</strong></p>
            {% if success %}
                <div class="badge success">Conexion a Base de Datos Exitosa</div>
                <p style="margin-top: 10px; color: #334155;">{{ message }}</p>
            {% else %}
                <div class="badge error">Error conectando a MySQL</div>
                <p style="margin-top: 10px; font-size: 12px; color: #dc2626;">{{ message }}</p>
                <p style="font-size: 13px; color: #6b7280;">(Si acabas de iniciar el contenedor, MySQL tarda unos segundos en inicializarse. Espera 10 segundos y refresca la pagina).</p>
            {% endif %}
            <p class="info">Servicios: Web (Flask/Python) y DB (MySQL 8.0)</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, success=success, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
