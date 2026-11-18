from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Fixture 3 Canchas - 3 partidos por equipo</title></head>
<body>
    <h1>Generador de Fixture (3 partidos por equipo)</h1>
    <form method="POST">
        <label>Equipos (separados por coma):</label><br>
        <textarea name="equipos" rows="4" cols="60">A,B,C,D,E,F,G,H</textarea><br><br>
        <input type="submit" value="Generar Fixture">
    </form>
    {% if fixture %}
        <h2>Fixture generado</h2>
        {% for fecha, partidos in fixture.items() %}
            <h3>{{ fecha }}</h3>
            <ul>
            {% for cancha, partido in partidos.items() %}
                <li><strong>{{ cancha }}:</strong> {{ partido }}</li>
            {% endfor %}
            </ul>
        {% endfor %}
    {% endif %}
    {% if error %}
        <p style="color:red">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

def generar_fixture(equipos):
    """Genera un fixture donde cada equipo juega exactamente 3 partidos."""
    n = len(equipos)
    if n < 4:
        return None, "Se necesitan al menos 4 equipos para que cada uno juegue 3 partidos."

    # Generar enfrentamientos: cada equipo i juega contra i+1, i+2, i+3 (circular)
    enfrentamientos = set()
    for i in range(n):
        for offset in [1, 2, 3]:
            j = (i + offset) % n
            if i != j:
                # Evitar duplicados (A vs B = B vs A)
                par = tuple(sorted([equipos[i], equipos[j]]))
                enfrentamientos.add(par)

    # Convertir a lista y ordenar para un calendario estable
    partidos = list(enfrentamientos)
    partidos.sort()

    # Distribuir en fechas: 3 canchas por fecha (3 partidos por fecha)
    fixture = {}
    canchas = ["Cancha 1", "Cancha 2", "Cancha 3"]
    fecha_num = 1
    for i in range(0, len(partidos), 3):
        bloque = partidos[i:i+3]
        fecha = f"Fecha {fecha_num}"
        fixture[fecha] = {}
        for j, (eq1, eq2) in enumerate(bloque):
            fixture[fecha][canchas[j]] = f"{eq1} vs {eq2}"
        fecha_num += 1

    return fixture, None

@app.route("/", methods=["GET", "POST"])
def index():
    fixture = None
    error = None
    if request.method == "POST":
        equipos_input = request.form.get("equipos", "")
        equipos = [e.strip() for e in equipos_input.split(",") if e.strip()]
        fixture, error = generar_fixture(equipos)
    return render_template_string(HTML, fixture=fixture, error=error)

if __name__ == "__main__":
    app.run(debug=True)