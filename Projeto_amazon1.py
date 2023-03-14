from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import os
from time import sleep

# Função padrao para iniciar o WebDriver
def iniciar_driver():

    # Cria uma variavel para armezanar a função Options
    chrome_options = Options()


    # cria uma lista com os parametros da options, no final do programa temos uma lista
    arguments = ['--lang=pt-BR','--window-size=500,500','--incognito']

    # Add os argumentos da lista arguments na variavel chrome_options
    for argument in arguments:
        chrome_options.add_argument(argument)


    # Configurações experimentais, sempre carrega-las
    chrome_options.add_experimental_option('prefs',{
    # alterar o local padrao de download de arquivos
    # 'download.default_directory' : 'local',
    # notificar o google chrome sobre essa alteração
    'download.directory_upgrade' : True,
    # desabilita a confirmação de dowload
    'download.prompt_for_download': False,
    # Desabilitar notificações
    'profile.default_content_setting_values.notifications' :2,
    # Permite multiplos downloads
    'profile.default_content_setting_values.automatic_downloads' : 1
    })

    


    # Inicializa o webdriver e carrega o chrome_optons
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

    return driver


# Carrega os parametros da função iniciar_driver() e maximiza a tela
driver  = iniciar_driver()
driver.maximize_window()

# acessar o site da amazon, guia kindle e garantir que todos os dados sejam carregados
driver.get('https://www.amazon.com.br/s?k=kindle&i=amazon-devices&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=BNLXA8HOMS58&sprefix=kindle%2Camazon-devices%2C206&ref=nb_sb_noss_1')


sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(5)

# Pegar o titulo do anuncio
titulos = driver.find_elements(By.XPATH,"//span[@class='a-size-medium a-color-base a-text-normal']")
sleep(5)


# Pegar o preço do kindle
precos = driver.find_elements(By.XPATH,"//span[@class='a-price-whole']")

# Pegar os centavos do Kindle
preco_centavos = driver.find_elements(By.XPATH,"//span[@class='a-price-fraction']")

# link do anuncio
links_anuncios = driver.find_elements(By.XPATH,"//a[@class='a-link-normal s-no-outline']")
links_anuncios.pop(0)
ponto = '.'
for titulo, preco, preco_centavo,link in zip(titulos, precos,preco_centavos,links_anuncios):
    preco_total = preco.text + ponto + preco_centavo.text
    with open('kindle.csv','a',encoding='utf-8',newline='') as arquivo:
        link_processado = link.get_attribute('href')
        arquivo.write(f'{titulo.text.replace(","," ")};{preco_total};{link_processado}  {os.linesep}')
print('Termino')
input('')

# titulo.text.replace(","," ") Fiz isso para evitar que o .csv separe o titulo com as virgulas

