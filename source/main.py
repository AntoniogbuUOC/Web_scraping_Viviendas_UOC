import time
import multiprocessing
import warnings

from selenium import webdriver
import pandas as pd

from scrappingFunctions import cierraCookies, login, rellenaPrimerInput, infinite_scroll, scrapping, existeSiguiente, presionaSiguiente, join_data

#----------------------------------------
# FUNCIONES
#----------------------------------------

# Función chrome: ejecuta el driver de Google Chrome y abre una nueva tab con una determinada configuración
def chrome(headless=False):
    # User Agent Mac de Antonio:
    #headers_antonio={ 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    # User Agent Windows de Mario:
    #headers_mario={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance' : 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument('--headless')
    # En caso de ser necesario User Agent
    # User Agent de Antonio
    # driverAntonio = webdriver.Chrome(PATH, options = opt, desired_capabilities=d, headers_antonio)
    # User Agent de Mario
    # driverMario = webdriver.Chrome(PATH, options = opt, desired_capabilities=d, headers_mario)
    driver = webdriver.Chrome(PATH, options = opt, desired_capabilities=d)
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(60)
    opt.add_argument('--incognito')
    return driver

# Función scrappingProcess: realiza todo el proceso de navegación y scrapping del sitio Web
def scrappingProcess(location):
    # 0º) Se inicializa el driver de chrome
    driver = chrome(headless=False)
    # 1º) Se busca la url en el driver
    driver.get('https://www.fotocasa.es')
    time.sleep(0.5)
    # 2º) Se cierra el panel de cookies
    cierraCookies(driver)
    time.sleep(2)
    # 3º) Se rellenan las credenciales del usuario y se logea al bot en la web
    login(driver)
    time.sleep(2)
    # 4º) Se rellena el primer input con el código postal
    rellenaPrimerInput(location,driver)
    time.sleep(4)
    siguiente = True
    # 6º) Bucle while que ejecuta el proceso hasta que no encuentre más páginas en las que buscar
    numPagina = 1
    while siguiente==True:
        # 0º) Se crea el dataFrame que va a guardar la información
        dfPantalla = pd.DataFrame()
        # 6.1) Se recorre la página entera para poder cargar correctamente todo el hmtl
        infinite_scroll(driver)
        time.sleep(2)
        # 6.2) Se scrapean todas las viviendas y sus propiedades
        casa = scrapping(driver)
        # 6.4) Se añaden los datos al df de la pantalla y se añade la columna location
        dfPantalla = pd.concat([dfPantalla, casa], axis=0)
        dfPantalla['Localidad'] = location
        # 6.5) Se guarda el dataFrame en un csv
        dfPantalla.to_csv('data/'+str(location)+'_'+str(numPagina)+'.csv')
        numPagina += 1
        # 6.5) Se consulta si existe una página siguiente
        siguiente = existeSiguiente(driver)
        # 6.6) En caso posible, se avanza a la siguiente página
        presionaSiguiente(driver)
        time.sleep(2)
    # 9) Se cierra el navegador
    driver.close()
    driver.quit()


#----------------------------------------
# VARIABLES
#----------------------------------------
warnings.filterwarnings("ignore")
# Número de procesos que se ejecutarán en simultáneo
hilosSimultaneos = 15
# Ubicación del driver
PATH = "drivers/Windows/chromedriver"
#PATH = "../drivers/Mac/chromedriver"
# Lista de localidades
lista_localidad = pd.read_csv('cfg/localidades.csv')

#----------------------------------------
# MAIN
#----------------------------------------
if __name__=='__main__':
    # 1º) Se recorren las filas del fichero de localidades con pasos según la cantidad indicado en la variable hilosSimultaneos
    for i in range(0,len(lista_localidad),hilosSimultaneos):
        for j in range(hilosSimultaneos):
            # Se crea cada proceso
            p=multiprocessing.Process(target=scrappingProcess,args=(lista_localidad.iloc[i+j]['localidad'],))
            # Se inicia cada procesos
            p.start()
        # Se espera a que se acaben todos los procesos simultáneos
        p.join()
    # Se espera una cantidad razonable de tiempo a que terminen el resto de procesos
