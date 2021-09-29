from kiwiscripts import fsel
import func_texto

def getPreguntasGoogleUnderDash(keyword, driver):
    # cargamos q=
    driver.get('https://www.google.es/search?q='+keyword.replace(" ","+"))

    # click en search input
    fsel.click(driver, "//input[@aria-label='Buscar']")

    preguntas_ok = []

    preguntas = driver.find_elements_by_xpath("//li[@class='sbct']/*/div[@role='option']/div[1]/span")
    for pregunta in preguntas:
        if func_texto.comprobarKwEnTexto(keyword, pregunta.text):
            preguntas_ok.append(pregunta.text)

    if len(preguntas_ok) > 0:
        # creamos array
        return preguntas_ok
    else:
        return None

def getPreguntasGoogle(keyword, driver=None, kw_en_preguntas=None):
    # busca las principales busquedas relacionadas de la kw en google

    # si no cargamos un driver, abrimos
    if driver is None:
        optsWindowed = Options()
        optsWindowed.add_argument("log-level=3")
        #optsWindowed.add_argument("--headless")
        optsWindowed.add_argument("--incognito")
        #optsWindowed.add_argument("user-data-dir="+ruta_perfil_chrome.replace("PERFIL",nombre_usuario_local))
        driver = webdriver.Chrome('chromedriver.exe', chrome_options=optsWindowed)
    
    driver.get('https://www.google.es/search?q='+keyword.replace(" ","+"))

    if driver is None:
        fsel.ver(driver, "//div[@class='jyfHyd'][contains(text(),'Acepto')]")
        fsel.click(driver, "//div[@class='jyfHyd'][contains(text(),'Acepto')]")

    # cogemos las preguntas de los users (google)
    try:
        preguntas_google = driver.find_elements_by_xpath("//div[@jsname='jIA8B']/span")
    except Exception as e:
        preguntas_google = []

    if driver is None:
        driver.quit()

    if len(preguntas_google) > 0:
        # creamos array
        preguntas = []
        for pregunta in preguntas_google:
            if kw_en_preguntas is None:
                preguntas.append(pregunta.text)
            else:
                if func_texto.comprobarKwEnTexto(keyword, func_texto.limpiarTexto(pregunta.text)):
                    preguntas.append(pregunta.text)

        if len(preguntas) > 0:
            return preguntas
        else:
            return None
    else:
        return None