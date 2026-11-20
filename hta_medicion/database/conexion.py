import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "hta.db"


def conectar():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        raise Exception(
            f"Error de conexión a la base de datos:\n{e}"
        )


def crear_bd():

    conn = conectar()

    try:

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mediciones(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            sistolica INTEGER NOT NULL,
            diastolica INTEGER NOT NULL,
            pulsaciones INTEGER NOT NULL,
            glucosa INTEGER NOT NULL DEFAULT 0,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
            registrado_por INTEGER NOT NULL REFERENCES usuarios(id),
            observacion TEXT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("PRAGMA table_info(mediciones)")
        columnas = {
            fila[1]
            for fila in cursor.fetchall()
        }
        if "glucosa" not in columnas:
            cursor.execute("""
                ALTER TABLE mediciones
                ADD COLUMN glucosa INTEGER NOT NULL DEFAULT 0
            """)

        if "usuario_id" not in columnas:
            cursor.execute("""
                ALTER TABLE mediciones
                ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id)
            """)

        if "registrado_por" not in columnas:
            cursor.execute("""
                ALTER TABLE mediciones
                ADD COLUMN registrado_por INTEGER REFERENCES usuarios(id)
            """)

        conn.commit()

    except sqlite3.Error as e:

        raise Exception(
            f"Error creando tablas:\n{e}"
        )

    finally:
        conn.close()


def asignar_mediciones_anteriores_a_admin():
    conn = conectar()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ?",
            ("admin",)
        )
        admin = cursor.fetchone()
        if admin is None:
            raise Exception("No existe el usuario admin para migrar las mediciones.")

        cursor.execute("""
            UPDATE mediciones
            SET usuario_id = COALESCE(usuario_id, ?),
                registrado_por = COALESCE(registrado_por, ?)
            WHERE usuario_id IS NULL
               OR registrado_por IS NULL
        """, (admin[0], admin[0]))
        conn.commit()

    except sqlite3.Error as e:
        raise Exception(
            f"Error asignando las mediciones existentes a admin:\n{e}"
        )

    finally:
        conn.close()