import time
import re
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.binary_location = "/usr/bin/google-chrome"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

NOMBRE = "Javiera Pizarro"
FECHA = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

datos_base = []
datos_finales = []
TOTAL_PAGINAS = 50

for pagina in range(1, TOTAL_PAGINAS + 1):
    url = f"https://www.clicar.cl/vehiculos/usado?page={pagina}"
    print("📄 Página:", pagina)

    driver.get(url)
    time.sleep(5)

    autos = driver.find_elements(By.CSS_SELECTOR, "li.h-fit")
    print("Autos en página:", len(autos))

    for auto in autos:
        try:
            texto = auto.text.strip()
            lineas = [x.strip() for x in texto.split("\n") if x.strip()]
            link = auto.find_element(By.TAG_NAME, "a").get_attribute("href")

            partes_url = link.split("/marcas/")[1].split("/")
            marca = partes_url[0].replace("-", " ").title()

            slug = partes_url[2]
            slug = re.sub(r"-\d+$", "", slug)
            slug = slug.replace(partes_url[0] + "-", "")
            modelo = slug.replace("-", " ").title()

            texto_completo = " ".join(lineas)

            match_anio = re.search(r"\b(20\d{2})\b", texto_completo)
            anio = match_anio.group(1) if match_anio else None

            match_km = re.search(r"(\d{1,3}(?:\.\d{3})*)\s*Km", texto_completo, re.IGNORECASE)
            kilometraje = match_km.group(1) + " Km" if match_km else None

            precio = None
            for i, linea in enumerate(lineas):
                if linea == "$" and i + 1 < len(lineas):
                    precio = "$" + lineas[i + 1]
                    break

            datos_base.append({
                "marca": marca,
                "modelo": modelo,
                "anio": anio,
                "kilometraje": kilometraje,
                "combustible": "No especificado",
                "ciudad": "No disponible",
                "url": link,
                "precio": precio,
                "nombre": NOMBRE,
                "fecha_captura": FECHA
            })

        except:
            continue

print("Datos base:", len(datos_base))

for dato in datos_base:
    try:
        driver.get(dato["url"])
        time.sleep(2)

        texto_original = driver.find_element(By.TAG_NAME, "body").text
        texto = texto_original.lower()

        ciudad = "No disponible"
        for linea in texto_original.split("\n"):
            if "," in linea and "vehículo" not in linea.lower():
                posible_ciudad = linea.split(",")[-1].strip()
                if 2 < len(posible_ciudad) < 40:
                    ciudad = posible_ciudad
                    break

        if "gasolina" in texto:
            combustible = "Gasolina"
        elif "diesel" in texto or "diésel" in texto:
            combustible = "Diesel"
        elif "híbrido" in texto or "hibrido" in texto:
            combustible = "Híbrido"
        elif "eléctrico" in texto or "electrico" in texto:
            combustible = "Eléctrico"
        elif "petróleo" in texto or "petroleo" in texto:
            combustible = "Petróleo"
        else:
            combustible = "No especificado"

        dato["ciudad"] = ciudad
        dato["combustible"] = combustible

        dato_ordenado = {
            "marca": dato["marca"],
            "modelo": dato["modelo"],
            "anio": dato["anio"],
            "kilometraje": dato["kilometraje"],
            "combustible": dato["combustible"],
            "ciudad": dato["ciudad"],
            "url": dato["url"],
            "precio": dato["precio"],
            "nombre": dato["nombre"],
            "fecha_captura": dato["fecha_captura"]
        }

        datos_finales.append(dato_ordenado)
        

    except:
        datos_finales.append(dato)

driver.quit()

client = MongoClient("mongodb://mongodb:27017/")
db = client["proyecto_bigdata"]
coleccion = db["datos_scraping"]

for dato in datos_finales:
    coleccion.update_one(
        {"url": dato["url"]},
        {"$set": dato},
        upsert=True
    )

print("🔥 LISTO")
print("📦 Total en Mongo:", coleccion.count_documents({}))
