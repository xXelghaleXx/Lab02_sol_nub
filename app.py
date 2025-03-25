from flask import Flask, render_template
import psycopg2
import os
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
app = Flask(__name__, template_folder='plantilla')

# Conexión directa a PostgreSQL
def get_db():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )

# Ruta principal con plantilla
@app.route('/')
def index():
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Obtener datos de ejemplo
        cur.execute("SELECT * FROM usuarios;")
        usuarios = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template('index.htm', usuarios=usuarios)
        
    except Exception as e:
        return f"""
        <h1>Error</h1>
        <p>{str(e)}</p>
        <p><b>Soluciones:</b></p>
        <ol>
            <li>Verifica que PostgreSQL esté activo</li>
            <li>Revisa el archivo .env</li>
            <li>Asegúrate que exista la tabla 'usuarios'</li>
        </ol>
        """, 500

if __name__ == '__main__':
    app.run(debug=True)