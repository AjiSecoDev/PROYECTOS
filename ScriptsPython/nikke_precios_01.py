import requests
from bs4 import BeautifulSoup

URL = "https://www.nike.com.pe/productos/calzado/hombre?start=0&sz=108"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

productos = soup.find_all("div", class_="region col-6 col-lg-4")

for producto in productos:
    # CONTENEDORES
    tile = producto.find("div", class_="product-tile")
    if tile:
        titulo = tile.find("h2", class_="product-title").get_text(strip=True)
        subtitulo = tile.find("h3", class_="product-subtitle").get_text(strip=True)
        enlace_tag = tile.find("a", href=True)
        enlace = "https://www.nike.com.pe" + enlace_tag['href'] if enlace_tag else ""
        
        # PRECIOS
        precio_tag = tile.find("span", class_="value")
        precio = precio_tag.get_text(strip=True) if precio_tag else "No disponible"

        # DESCUENTOS
        descuento_tag = tile.find("div", class_="discount")
        descuento = descuento_tag.get_text(strip=True) if descuento_tag else "0%"

        print(f"Producto: {titulo}")
        print(f"Subtítulo: {subtitulo}")
        print(f"Precio: {precio}")
        print(f"Descuento: {descuento}")
        print(f"Enlace: {enlace}")
        print("-" * 50)
