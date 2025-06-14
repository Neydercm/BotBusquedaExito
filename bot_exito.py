from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Confi navegador Brave
options = Options()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
options.add_argument("--disable-logging")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service('driver/chromedriver.exe')
bot = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(bot, 10)

# abre pag Éxito
bot.get("https://www.exito.com/")
bot.maximize_window()
time.sleep(2)

# Buscar  'iPhone'
busqueda = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-page"]/section/div/div[1]/div[2]/form/input')))
busqueda.send_keys("iPhone")
busqueda.submit()
time.sleep(5)

print("\nAbre pag y buscar la palabra")

# seleccionar filtro
filtros_panel = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[1]/div[1]/div')))
bot.execute_script("arguments[0].scrollIntoView(true);", filtros_panel)
time.sleep(2)

# desplegable "Vendido por"
vendido_por_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="desktop-store-filter-button--25"]')))
vendido_por_button.click()
time.sleep(2)

# chuleable "Éxito"
exito_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="desktop-store-filter-Vendido por-Éxito"]')))
bot.execute_script("arguments[0].scrollIntoView(true);", exito_checkbox)
time.sleep(1)
exito_checkbox.click()
time.sleep(2)

# Aplicar filtro
aplicar_filtro = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[1]/div[2]/button')))
aplicar_filtro.click()
time.sleep(5)

print("\naplica filtro y cargan los prod")

# archivo CSV
ruta_csv = r"C:\Users\TOSHIBA\Documents\U\2025-1\todo los de construcion de software\BOT-prueba\productos_exito.csv"
with open(ruta_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre del Producto", "Precio"])

    def extraer_productos():
        nombres = bot.find_elements(By.CLASS_NAME, "styles_name__qQJiK")
        precios = bot.find_elements(By.CSS_SELECTOR, 'p[data-fs-container-price-otros="true"]')

        for nombre, precio in zip(nombres, precios):
            #print(f"Guardado: {nombre.text} - {precio.text}")
            writer.writerow([nombre.text, precio.text])

    # productos primera pág
    print("\nProductos primera página registrados")
    extraer_productos()

    # Scroll
    for y in range(0, 401, 100):
        bot.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(0.5)

    # Cambiar a segunda página
    siguiente_pagina_xpath = '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[3]/section/div/ul/li[2]/button'
    siguiente_btn = wait.until(EC.element_to_be_clickable((By.XPATH, siguiente_pagina_xpath)))
    siguiente_btn.click()
    print("\nPasando a la segunda página...")
    time.sleep(5)

    # products segunda pág
    print("\nProductos segunda página registrados")
    extraer_productos()

# pantallazo
time.sleep(1)
#bot.save_screenshot("pantallazo.png")
#bot.execute_script("window.scrollTo(0, 0);")

# Cerrar navegador
bot.quit()
print("\n✅ Datos recopilados, capturas tomadas y navegador cerrado.")
