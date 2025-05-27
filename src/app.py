import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# URL de la página que quieres descargar
url = " https://companies-market-cap-copy.vercel.app/index.html"

# Realizar la solicitud GET
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código 200)
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL de la página
url = "https://companies-market-cap-copy.vercel.app/index.html"

# Realizar la solicitud GET
response = requests.get(url)
response.raise_for_status()  # Verificar que la solicitud fue exitosa

# Parsear el HTML con BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Buscar todas las tablas en la página
tabla = soup.find("table")

# Extraer las filas 

rows = tabla.find_all("tr")

# Procesar datos de la tabla
data = []
for row in rows[1:]:  # Saltar la fila de encabezado
    cols = row.find_all("td")
    fecha = cols[0].text.strip()
    ingresos = cols[1].text.strip()
    data.append([fecha, ingresos])

# Crear un DataFrame con los datos extraídos
data = pd.DataFrame(data, columns=["Fecha", "Ingresos"])

# Ordenar los datos por la columna "Fecha" de menor a mayor 
data = data.sort_values("Fecha")

# Limpiar y convertir los ingresos a números
def convertir_ingresos(valor):
    if isinstance(valor,str):
        
        if "B" in valor:
         return float(valor.replace("B", "").replace("$", "").replace(",", ""))
    return valor  # Return the original value if it's already a number


data["Ingresos"] = data["Ingresos"].apply(convertir_ingresos)

data["Ingresos"]

# Conectar a SQLite y guardar los datos
conn = sqlite3.connect("tesla_revenues.db")
cursor = conn.cursor()

# Crear tabla en SQLite
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingresos (
    fecha TEXT,
    ingresos REAL
)
""")

# Insertar datos en la base de datos
for index, row in data.iterrows():
    cursor.execute("INSERT INTO ingresos (fecha, ingresos) VALUES (?, ?)", (row["Fecha"], row["Ingresos"]))

conn.commit()
conn.close()

# Graficar los datos
plt.figure(figsize=(10, 6))
plt.plot(data["Fecha"], data["Ingresos"], marker='o', label="Ingresos")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Fecha")
plt.ylabel("Ingresos en billones(USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Guardar y mostrar el gráfico
plt.savefig("revenue_plot.png")
plt.show()

