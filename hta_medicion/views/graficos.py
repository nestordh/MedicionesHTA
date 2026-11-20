import matplotlib.pyplot as plt

from models.medicion import Medicion


class GraficoPresion:

    @staticmethod
    def mostrar(usuario_id):
        datos = Medicion.estadisticas_completas(usuario_id)
        if not datos:
            raise Exception(
                "No existen registros."
            )

        fechas = []
        sistolicas = []
        diastolicas = []
        pulsaciones = []
        glucosa = []

        for r in datos:
            fechas.append(r[0])
            sistolicas.append(r[1])
            diastolicas.append(r[2])
            pulsaciones.append(r[3])
            glucosa.append(r[4])

        fig, (ax_presion, ax_pulso, ax_glucosa) = plt.subplots(
            3,
            1,
            figsize=(12, 9),
            sharex=True
        )

        ax_presion.plot(
            fechas,
            sistolicas,
            color="red",
            marker="o",
            label="Sistólica"
        )
        ax_presion.plot(
            fechas,
            diastolicas,
            color="blue",
            marker="o",
            label="Diastólica"
        )
        ax_presion.set_ylabel("Presión (mmHg)")
        ax_presion.set_title("Evolución de las mediciones")
        ax_presion.legend()

        ax_pulso.plot(
            fechas,
            pulsaciones,
            color="green",
            marker="o",
            label="Pulsaciones"
        )
        ax_pulso.set_ylabel("Pulsaciones")
        ax_pulso.legend()

        ax_glucosa.plot(
            fechas,
            glucosa,
            color="purple",
            marker="o",
            label="Glucosa"
        )
        ax_glucosa.set_ylabel("Glucosa (mg/dL)")
        ax_glucosa.legend()
        ax_glucosa.tick_params(axis="x", labelrotation=45)
        fig.tight_layout()
        plt.show()