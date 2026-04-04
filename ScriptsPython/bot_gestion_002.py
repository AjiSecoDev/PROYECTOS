#BOT QUE VERIFICA LAS NOTICIAS DE GESTION
  import requests
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
from aiogram import Bot

TOKEN = "1112222333:hola"      
CHAT_ID = 3456787654  
bot = Bot(token=TOKEN)

#scrap
URL = "https://gestion.pe/economia/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# NO repeticiones
enviadas = set()

async def obtener_noticias():
    """DICCIONARIO o csvvv"""
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        noticias = []

        # story-item
        stories = soup.find_all("div", class_="story-item")
        for story in stories:
            try:
                title_tag = story.find("a", class_="story-item__title")
                titulo = title_tag.text.strip() if title_tag else None
                link = title_tag["href"] if title_tag else None
                if link and link.startswith("/"):
                    link = "https://gestion.pe" + link

                # NO duplicados
                if link in enviadas:
                    continue

                author_tag = story.find("a", class_="story-item__author")
                author = author_tag.text.strip() if author_tag else None
                section_tag = story.find("a", class_="story-item__section")
                section = section_tag.text.strip() if section_tag else None
                date_elements = story.find_all("span", class_="story-item__date-time")
                fecha = date_elements[0].text.strip() if len(date_elements) > 0 else None
                hora = date_elements[1].text.strip() if len(date_elements) > 1 else None
                img_tag = story.find("img")
                imagen = img_tag["src"] if img_tag else None

                noticias.append({
                    "tipo": "normal",
                    "seccion": section,
                    "fecha": fecha,
                    "hora": hora,
                    "titulo": titulo,
                    "link": link,
                    "autor": author,
                    "imagen": imagen
                })
            except:
                continue

        # LOS DIVS DEL G
        featured = soup.find_all("div", class_="fs-wis")
        for item in featured:
            try:
                title_tag = item.find("h2", class_="fs-wis__title")
                titulo = title_tag.text.strip() if title_tag else None
                link_tag = item.find("a", class_="fs-wis__img-link")
                link = link_tag["href"] if link_tag else None
                if link and link.startswith("/"):
                    link = "https://gestion.pe" + link

                if link in enviadas:
                    continue

                section_tag = item.find("h3", class_="fs-section-label")
                section = section_tag.text.strip() if section_tag else None
                author_tag = item.find("address")
                author = author_tag.text.strip() if author_tag else None
                img_tag = item.find("img")
                imagen = img_tag["src"] if img_tag else None

                noticias.append({
                    "tipo": "destacado",
                    "seccion": section,
                    "fecha": None,
                    "hora": None,
                    "titulo": titulo,
                    "link": link,
                    "autor": author,
                    "imagen": imagen
                })
            except:
                continue

        return noticias

    except Exception as e:
        print("Error scraping:", e)
        return []


# FUNCION asyng del bot

async def enviar_alerta():
    while True:
        noticias = await obtener_noticias()
        for noticia in noticias:
            msg = f"📰 {noticia['titulo']}\nSección: {noticia['seccion']}\nAutor: {noticia['autor']}\nLink: {noticia['link']}"
            try:
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                print(f"Enviado: {noticia['titulo']}")
                enviadas.add(noticia['link'])
            except Exception as e:
                print(f"Error enviando mensaje: {e}")

        await asyncio.sleep(3600)  # cambiar (en segundos)

#PARA EJECUTAR
async def main():
    await enviar_alerta()

if __name__ == "__main__":
    asyncio.run(main())
