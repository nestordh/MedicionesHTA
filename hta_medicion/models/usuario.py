from database.conexion import conectar
from utils.seguridad import (
    hash_password,
    verificar_password
)

import sqlite3


class Usuario:

    @staticmethod
    def crear_admin():

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE usuario = ?
            """, ("admin",))

            existe = cursor.fetchone()

            if not existe:

                password = hash_password("admin")

                cursor.execute("""
                INSERT INTO usuarios
                (
                    usuario,
                    password
                )
                VALUES (?,?)
                """,
                (
                    "admin",
                    password
                ))

                conn.commit()

        except sqlite3.Error as e:

            raise Exception(
                f"Error creando administrador:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def login(usuario, password):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE usuario = ?
            """, (usuario,))

            usuario_db = cursor.fetchone()

            if usuario_db is None:
                return False

            password_hash = usuario_db[2]

            return verificar_password(
                password,
                password_hash
            )

        except sqlite3.Error as e:

            raise Exception(
                f"Error en login:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def obtener_id(usuario):
        conn = conectar()

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM usuarios WHERE usuario = ?",
                (usuario,)
            )
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None

        except sqlite3.Error as e:
            raise Exception(
                f"Error obteniendo el usuario:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def listar_usuarios():
        conn = conectar()

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario
                FROM usuarios
                ORDER BY usuario COLLATE NOCASE
            """)
            return cursor.fetchall()

        except sqlite3.Error as e:
            raise Exception(
                f"Error listando usuarios:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def crear_usuario(usuario, password):

        conn = conectar()

        try:

            cursor = conn.cursor()

            password_hash = hash_password(password)

            cursor.execute("""
            INSERT INTO usuarios
            (
                usuario,
                password
            )
            VALUES (?,?)
            """,
            (
                usuario,
                password_hash
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            raise Exception(
                "El usuario ya existe."
            )

        except sqlite3.Error as e:

            raise Exception(
                f"Error creando usuario:\n{e}"
            )

        finally:
            conn.close()