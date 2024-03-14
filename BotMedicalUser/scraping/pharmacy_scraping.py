from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import json

# Classe para serviços de farmácia
class PharmacyService():
    def __init__(self):
        # Configurações do navegador Chrome
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument("--window-size=1200,1000")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        self.driver = None
        self.service = None
        self.pharmacy_url = ["https://www.drogaraia.com.br/search?w=","&origin=&ranking=&p=1&facets=c-2%3A3-0-10"]

        # Listas para armazenar informações dos produtos
        self.title_product = list()
        self.name_manufacturer = list()
        self.porcent = list()
        self.price_from = list()
        self.price_final = list()
        self.url_image = list()
        self.url_product =list()

    # Método para obter informações dos produtos
    def get_products(self, remedy_name):
        # Configurações do serviço do Chrome WebDriver
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service,options=self.chrome_options)
        url = self.pharmacy_url[0] + remedy_name + self.pharmacy_url[1]
        self.driver.get(url)

        # Verificando se o cookie é visível
        cooquie = self.get_cookie()
        if cooquie:
            # Localizando elementos do produto na página
            xpath = '/html/body/div[1]/main/div[3]/div/div[2]/div[3]'
            class_name = 'ProductGridstyles__ProductGridStyles-sc-1wbcxrt-0 jkDOLa'
            products_result = self.find_element_by_xpath_or_class(xpath, class_name)

            if products_result:
                products = products_result.find_elements(By.CLASS_NAME, 'product-item')[:1]
                for product in products:
                    # Obtendo informações do produto
                    self.get_porcent(product)
                    self.get_title_remedy(product)
                    self.get_manufacturer(product)
                    self.get_price_from(product)
                    self.get_price_final(product)
                    self.get_url_image(product)
                    self.get_url_product(product)

                    # Criando e respondendo com um JSON contendo informações do produto
                    data_json = self.creat_and_response_json()
                    self.driver.quit()
                    return data_json
            
            else:
                self.driver.quit()
                return False
        else:
            self.driver.quit()
            return False
        
    # Método para localizar elementos por xpath ou classe
    def find_element_by_xpath_or_class(self, xpath, class_name):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
                )
                return element
            except TimeoutException:
                return False

    # Método para obter o cookie e remover o elemento de cookie visível
    def get_cookie(self):
        try:
            elemento_visivel = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]'))
            )
            sleep(1)
            cooquie = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[1]')
            self.driver.execute_script("arguments[0].remove();", cooquie)
            return True
        except TimeoutException:
            print("Tempo de espera expirado. Elemento não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao tentar pegar o cookie: {e}")
            return False
    
    # Métodos para obter informações específicas do produto
    def get_porcent(self, product):
        try:
            porcent = product.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div[1]/div[1]/div/span')

            if porcent:
                self.porcent.append(porcent.text)
        except Exception as e:
            self.porcent.append('N/F')

    def get_title_remedy(self, product):
        try:
            title = product.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div[1]/h2/a')
            if title:
                self.title_product.append(title.get_attribute('title'))
        except Exception as e:
            self.title_product.append('N/F')

    def get_manufacturer(self, product):
        try:
            manufacturer = product.find_element(By.CLASS_NAME, 'product-brand')
                    
            if manufacturer:
                self.name_manufacturer.append(manufacturer.text)
        except Exception as e:
            self.name_manufacturer.append('N/F')

    def get_price_from(self, product):
        try:
            price_from = product.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div[1]/div[7]/div[1]/div[1]/span/div')
                    
            if price_from:
                self.price_from.append(price_from.text)
        except Exception as e:
            self.price_from.append('N/F')

    def get_price_final(self, product):
        try:
            price_final = product.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div[1]/div[7]/div[1]/div[2]/span/div')
                    
            if price_final:
                self.price_final.append(price_final.text)
        except Exception as e:
            self.price_final.append('N/F')

    def get_url_image(self, product):
        try:
            url_image = product.find_element(By.CLASS_NAME, 'ProductCardImagestyles__ProductImage-sc-1dv85s1-1')

            if url_image:
                self.url_image.append(url_image.get_attribute('src'))
        except Exception as e:
            self.url_image.append('N/F')

    def get_url_product(self, product):
        try:
            url_product = product.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div[1]/h2/a')

            if url_product:
                self.url_product.append(url_product.get_attribute('href'))
        except Exception as e:
            self.url_product.append('N/F')

    # Método para criar e retornar um JSON com as informações dos produtos
    def creat_and_response_json(self):         
        data = {
            "title_product": self.title_product,
            "name_manufacturer": self.name_manufacturer,
            "porcent": self.porcent,
            "price_from": self.price_from,
            "price_final": self.price_final,
            "url_image": self.url_image,
            "url_product": self.url_product
        }

        json_data = json.dumps(data, indent=4)
        return json_data
