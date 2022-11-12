from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
from os import remove
import pandas as pd
import time


# Función cierraCookies: cierra el mensaje emergente sobre si el usuairo desea aceptar o rechazar las cookies
def cierraCookies(driver):
    botonCookies = driver.find_element(By.XPATH, '//*[@id="App"]/div[3]/div/div/div/footer/div/button[2]')
    botonCookies.click()

# Función  login: logea al bot en la web de fotocasa con las credenciales correspondientes
def login(driver):
    credentialsFile = pd.read_csv('cfg/credentials.csv')
    user = credentialsFile.iloc[0]['user']
    password = credentialsFile.iloc[0]['password']
    loginbutton = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/header/div[3]/div[5]/button')
    loginbutton.click()
    time.sleep(1.5)
    input_user = driver.find_element(By.XPATH, '//*[@id="gigya-login-form"]/div[1]/div[2]/input')
    input_user.send_keys(user)
    time.sleep(0.75)
    input_password = driver.find_element(By.XPATH, '//*[@id="gigya-login-form"]/div[1]/div[3]/input')
    input_password.send_keys(password)
    access_login = driver.find_element(By.XPATH, '//*[@id="gigya-login-form"]/div[1]/div[4]/input')
    access_login.click()

# Función rellenaPrimerInput: una vez logeado el usuario, introduce el nombre de la población en el buscador
def rellenaPrimerInput(location, driver):
    primerInput = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/header/div[2]/form/div/div/div/div/div/input')
    for i in location:
        primerInput.send_keys(i)
        time.sleep(0.2)
    time.sleep(0.5)
    down = primerInput.send_keys(Keys.DOWN)
    time.sleep(1)
    down = driver.find_element(By.XPATH, '//*[@id="App"]/div[1]/header/div[2]/form/div/div/div/ul/li')
    down.click()

# Función infinite_scroll: hace scroll hasta el final de la página para que se carge el html completo y se puedan leer todos los datos
def infinite_scroll(driver):
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(1)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            for i in range(100):
                driver.execute_script("window.scrollBy(0,0)","")
            break

# Función scrapping: extrae todas las propiedades de cada una de las viviendas de la página
def scrapping(driver):
    casas = {}
    df_casas = pd.DataFrame(columns=['URL', 'Imagen', 'Titulo', 'Inmobiliaria','Precio','Descripcion','Fecha'])
    soup = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(2)
    contenedor = soup.find_all(class_="re-CardPackMinimal")
    time.sleep(2)
    for i in range(len(contenedor)):
        element= contenedor[i]
        #URL
        fotocasa_url = 'https://www.fotocasa.es'
        if (element.find(class_="re-CardPackMinimal-slider") is None):
            casas['URL'] = ''
        else:
            casas['URL'] = fotocasa_url + element.find(class_="re-CardPackMinimal-slider").get('href')
        #Imagen
        if (element.find(class_="re-CardMultimediaSlider-image") is None):
            casas['Imagen'] = ''
        else:
            casas['Imagen'] =  element.find(class_="re-CardMultimediaSlider-image").get('src')
        #Titulo
        if (element.find(class_="re-CardPackMinimal-slider") is None):
            casas['Titulo'] = ''
        else:
            casas['Titulo'] = element.find(class_="re-CardPackMinimal-slider").get('title')
        #Inmobiliaria
        if (element.find(class_="re-CardPromotionLogo-link") is None):
            casas['Inmobiliaria'] = ''
        else:
            casas['Inmobiliaria'] = element.find(class_="re-CardPromotionLogo-link").img.get('alt')
        #Precio
        if (element.find(class_="re-CardPrice") is None):
            casas['Precio'] = ''
        else:
            casas['Precio'] = element.find(class_="re-CardPrice").get_text()
        #Propiedades
        if (element.find(class_="re-CardFeatures-wrapper") is None):
            casas['Propiedades'] = ''
        else:
            casas['Propiedades'] = ''
            propiedades = element.find(class_="re-CardFeatures-wrapper").find_all(class_="re-CardFeatures-feature")
            for i in range(len(propiedades)):
                casas['Propiedades'] = casas['Propiedades'] + ',' + propiedades[i].get_text()
        #Descripcion
        if (element.find("span", {"class": "re-CardDescription-text"}) is None):
            casas['Descripcion'] = ''
        else:
            casas['Descripcion'] = element.find("span", {"class": "re-CardDescription-text"}).get_text()
        #Fecha
        if (element.find("span", {"class": "re-CardTimeAgo"}) is None):
            casas['Fecha'] = ''
        else:
            casas['Fecha'] = element.find("span", {"class": "re-CardTimeAgo"}).get_text()
        time.sleep(0.5)
        df_casas = df_casas.append(casas,ignore_index=True)
    return df_casas

# Función existeSiguiente: comprueba si existen más páginas sobre viviendas de esa zona geográfica
def existeSiguiente(driver):
    url_actual = driver.current_url
    soup = BeautifulSoup(driver.page_source, "html.parser")
    next_page = soup.find_all(class_="sui-MoleculePagination-item")
    cadena = ""
    for x in next_page:
        cadena += (str(x))
    li = str(cadena).split('<li class="')
    flecha = str(li[-1]).split('href="')
    href = flecha[1].split('"')[0]
    if (url_actual != 'https://www.fotocasa.es' + href):
        return True
    else:
        return False

# Función presionaSiguiente: hace click sobre el botón de siguiente página en caso de que exista
def presionaSiguiente(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    next_page = soup.find_all(class_="sui-MoleculePagination-item")
    cadena = ""
    for x in next_page:
        cadena += (str(x))
    li = str(cadena).split('<li class="')
    flecha = str(li[-1]).split('href="')
    href = flecha[1].split('"')[0]
    driver.get('https://www.fotocasa.es' + href)

# Función join_data: se encarga de unir los ficheros obtenidos en cada una de las búsquedas en un fichero final
def join_data(lista_localidad):
    df_final = pd.DataFrame(columns=['URL', 'Imagen', 'Titulo', 'Inmobiliaria','Precio','Descripcion','Fecha'])
    for i in range(len(lista_localidad)):
        data = pd.read_csv('data/viviendas'+str(lista_localidad.iloc[i]['localidad'])+'.csv')
        path = 'data/viviendas'+str(lista_localidad.iloc[i]['localidad'])+'.csv'
        df_final = pd.concat([df_final,data]).reset_index(drop=True)
        remove(path)
    return df_final
