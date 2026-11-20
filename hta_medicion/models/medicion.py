from database.conexion import conectar

import sqlite3


class Medicion:

    @staticmethod
    def validar(
        sistolica,
        diastolica,
        pulsaciones
    ):

        if sistolica <= diastolica:

            raise ValueError(
                "La sistólica debe ser mayor que la diastólica."
            )

        if sistolica < 70 or sistolica > 250:

            raise ValueError(
                "Sistólica fuera de rango."
            )

        if diastolica < 40 or diastolica > 150:

            raise ValueError(
                "Diastólica fuera de rango."
            )

        if pulsaciones < 35 or pulsaciones > 220:

            raise ValueError(
                "Pulsaciones fuera de rango."
            )

    @classmethod
    def guardar(
        cls,
        fecha,
        hora,
        sistolica,
        diastolica,
        pulsaciones,
        glucosa,
        observacion,
        usuario_id,
        registrado_por
    ):

        cls.validar(
            sistolica,
            diastolica,
            pulsaciones
        )

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO mediciones
            (
                fecha,
                hora,
                sistolica,
                diastolica,
                pulsaciones,
                glucosa,
                usuario_id,
                registrado_por,
                observacion
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                fecha,
                hora,
                sistolica,
                diastolica,
                pulsaciones,
                glucosa,
                usuario_id,
                registrado_por,
                observacion
            ))

            conn.commit()

        except sqlite3.Error as e:

            raise Exception(
                f"Error guardando medición:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def listar(usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT
                m.id, m.fecha, m.hora, m.sistolica, m.diastolica,
                m.pulsaciones, m.glucosa, u.usuario,
                m.observacion, m.fecha_creacion
            FROM mediciones AS m
            LEFT JOIN usuarios AS u ON u.id = m.registrado_por
            WHERE m.usuario_id = ?
            ORDER BY m.fecha DESC,
                     m.hora DESC
            """, (usuario_id,))

            return cursor.fetchall()

        except sqlite3.Error as e:

            raise Exception(
                f"Error listando registros:\n{e}"
            )

        finally:
            conn.close()

    @classmethod
    def modificar(
        cls,
        id_registro,
        fecha,
        hora,
        sistolica,
        diastolica,
        pulsaciones,
        glucosa,
        observacion,
        usuario_id
    ):

        cls.validar(
            sistolica,
            diastolica,
            pulsaciones
        )

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE mediciones
            SET
                fecha=?,
                hora=?,
                sistolica=?,
                diastolica=?,
                pulsaciones=?,
                glucosa=?,
                observacion=?
            WHERE id=? AND usuario_id=?
            """,
            (
                fecha,
                hora,
                sistolica,
                diastolica,
                pulsaciones,
                glucosa,
                observacion,
                id_registro,
                usuario_id
            ))
            if cursor.rowcount == 0:
                raise Exception(
                    "No se encontró el registro."
                )
            conn.commit()
        except sqlite3.Error as e:
            raise Exception(
                f"Error modificando registro:\n{e}"
            )
        finally:
            conn.close()


    @staticmethod
    def eliminar(id_registro, usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM mediciones
            WHERE id = ? AND usuario_id = ?
            """,
            (id_registro, usuario_id))

            conn.commit()

        except sqlite3.Error as e:

            raise Exception(
                f"Error eliminando registro:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def maxima(usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT
                id, fecha, hora, sistolica, diastolica,
                pulsaciones, glucosa, observacion, fecha_creacion
            FROM mediciones
            WHERE usuario_id = ?
            ORDER BY sistolica DESC
            LIMIT 1
            """, (usuario_id,))

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def minima(usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT
                id, fecha, hora, sistolica, diastolica,
                pulsaciones, glucosa, observacion, fecha_creacion
            FROM mediciones
            WHERE usuario_id = ?
            ORDER BY sistolica ASC
            LIMIT 1
            """, (usuario_id,))

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def buscar_por_fecha(fecha_desde, fecha_hasta, usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    m.id, m.fecha, m.hora, m.sistolica, m.diastolica,
                    m.pulsaciones, m.glucosa, u.usuario,
                    m.observacion, m.fecha_creacion
                FROM mediciones AS m
                LEFT JOIN usuarios AS u ON u.id = m.registrado_por
                WHERE m.usuario_id = ?
                AND date(m.fecha)
                BETWEEN date(?)
                AND date(?)
                ORDER BY m.fecha ASC,m.hora ASC
            """,
            (
                usuario_id,
                fecha_desde,
                fecha_hasta
            ))

            return cursor.fetchall()

        except sqlite3.Error as e:

            raise Exception(
                f"Error buscando registros:\n{e}"
            )

        finally:
            conn.close()

    @staticmethod
    def obtener(id_registro, usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id, fecha, hora, sistolica, diastolica,
                    pulsaciones, glucosa, observacion, fecha_creacion
                FROM mediciones
                WHERE id = ? AND usuario_id = ?
            """,
            (id_registro, usuario_id)
            )

            return cursor.fetchone()

        finally:
            conn.close()


    @staticmethod
    def estadisticas(usuario_id):

        conn = conectar()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*),
                    AVG(sistolica),
                    AVG(diastolica),
                    AVG(pulsaciones),
                    MAX(sistolica),
                    MIN(sistolica),
                    AVG(NULLIF(glucosa, 0))
                FROM mediciones
                WHERE usuario_id = ?
            """, (usuario_id,))

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    # Promedios diarios
    def promedio_diario(usuario_id):
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    fecha,
                    ROUND(AVG(sistolica),0),
                    ROUND(AVG(diastolica),0),
                    ROUND(AVG(pulsaciones),0),
                    ROUND(AVG(NULLIF(glucosa, 0)),0)
                FROM mediciones
                WHERE usuario_id = ?
                GROUP BY fecha
                ORDER BY fecha
            """, (usuario_id,))
            return cursor.fetchall()
        finally:
            conn.close()


    @staticmethod
    # Estadísticas con datos para gráficos
    def estadisticas_completas(usuario_id):
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT
                fecha,
                sistolica,
                diastolica,
                pulsaciones,
                glucosa
            FROM mediciones
            WHERE usuario_id = ?
            ORDER BY fecha,hora
            """, (usuario_id,))
            return cursor.fetchall()
        finally:
            conn.close()










