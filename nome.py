# --- Imports necessários ---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gender_guesser.detector as gender
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 

from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd 


br_gender_info = gender.Detector(case_sensitive=False)


def scrape_trabalhos(url_alvo):
    """
    1. Abre o driver UMA VEZ.
    2. Acumula os trabalhos em uma lista.
    3. Clica em "Próximo" DEPOIS de raspar a página.
    4. Retorna a lista COMPLETA no final.
    """
    
    # 1. Configura o Service (Padrão Selenium 4)
    service = Service(ChromeDriverManager().install())

    options = Options()
    
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # --- Opções Anti-Detecção ---
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = None 
    
    # Lista para guardar TODOS os trabalhos de TODAS as páginas
    todos_os_trabalhos = []
    
    try:
        # 3. Inicializa o Driver
        driver = webdriver.Chrome(service=service, options=options)
        
        LOCATOR_PROXIMO = (By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/li[26]/a")
        LOCATOR_PROXIMO_url2 = (By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/li[18]/a")
        
        print(f"\n--- Processando URL (Headless): {url_alvo} ---")
        driver.get(url_alvo)
    
        wait = WebDriverWait(driver, 30) 
        
        locator_bloco = (By.CSS_SELECTOR, "a.link.info.pull-left")
        locator_titulo = (By.CSS_SELECTOR, ".titulo-trabalho.ng-binding")
        locator_autores = (By.CSS_SELECTOR, ".autores-anais.ng-binding")
        
       
        if url_alvo == "https://www.even3.com.br/anais/eneci2020/":
            LOCATOR_PROXIMO = LOCATOR_PROXIMO_url2

        time.sleep(10)
        while True:
            try:
                # 1. ESPERA OS BLOCOS DA PÁGINA ATUAL
                blocos_de_trabalho = wait.until(
                    EC.presence_of_all_elements_located(locator_bloco)
                )
                
                print(f"Encontrados {len(blocos_de_trabalho)} trabalhos na página atual...")

                # 2. RASPA OS BLOCOS DA PÁGINA ATUAL
                for bloco in blocos_de_trabalho:
                    
                    titulo_elements = bloco.find_elements(*locator_titulo)
                    titulo_texto = titulo_elements[0].text if titulo_elements else "N/A"
                    
                    autores_elements = bloco.find_elements(*locator_autores)
                    autores_lista = []
                    if autores_elements:
                        autores_string = autores_elements[0].text
                        autores_lista = [nome.strip() for nome in autores_string.split(';') if nome.strip()]
                    
                    link_url = bloco.get_attribute("href")
                    
                    trabalho_info = {
                        "titulo": titulo_texto,
                        "autores": autores_lista,
                        "link": link_url
                    }
                    todos_os_trabalhos.append(trabalho_info)
                
                # 3. TENTA ENCONTRAR E CLICAR EM "PRÓXIMO" 
                try:
                    wait_curto = WebDriverWait(driver, 5) 
                    
                    next_button = wait_curto.until(
                        EC.element_to_be_clickable(LOCATOR_PROXIMO)
                    )
                    
                    next_button.click()
                    print("Clicando em 'Próximo', carregando nova página...")
                    time.sleep(3) 
                    
                except (TimeoutException, NoSuchElementException):

                    print("Botão 'Próximo' não encontrado. Chegamos na última página.")
                    break # Quebra o loop 'while True'

            except Exception as e:
                print(f"Erro ao raspar a página. Detalhe: {e}")
                break # Quebra o loop 'while True' em caso de erro

        # 4. RETURN (DEPOIS que o loop 'while' quebrar)
        return todos_os_trabalhos
    
    finally:
        # 5. O 'finally' fecha o driver que foi aberto UMA VEZ
        if driver:
            driver.quit()
            print("Driver fechado.")


def scrape_lapef(url):
     # 1. Configura o Service (Padrão Selenium 4)
    service = Service(ChromeDriverManager().install())

    # 2. Configura as Opções
    options = Options()
    
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # --- Opções Anti-Detecção ---
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = None # Define o driver como None
    todos_os_trabalhos = []

    try:
        
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(5)

        wait = WebDriverWait(driver,60)
        main_div = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/main/div/div/div/article/div")) #Aguarda até a div principal que guarda todos os textos apareça na tela
        )
        main_div.find_elements(By.TAG_NAME, "p")
        p_tags = main_div.find_elements(By.TAG_NAME, "p") #captura os trabalhos que estão como tags p na div principal
            
        print(f"Encontrados {len(p_tags)} parágrafos. Processando...")

        for p  in p_tags:
            try:
                a_tag = p.find_element(By.TAG_NAME, "a")
                titulo = a_tag.text.strip()
                link = a_tag.get_attribute("href")
                if ".png" in link:
                    continue
                full_text = p.text.strip()
                authors_string = full_text.replace(titulo, "").strip()
                authors_string_cleaned = authors_string.replace(" e ", ", ").replace(" E ", ", ") #limpa e reorganiza o texto separando nome de autores para montar as listas
                authors_list = [
                    name.strip() for name in authors_string_cleaned.split(",") if name.strip() and name != "."
                ]
                trabalho_info = {
                    "titulo": titulo,
                    "autores": authors_list,
                    "link": link
                }
                todos_os_trabalhos.append(trabalho_info)

            except NoSuchElementException:
                print("a_tag não encontrado!")
                # Se um <p> não tiver um <a> (ex: <p>&nbsp;</p> ou texto de introdução),
                # ele será ignorado.
                continue 
                
        print(f"todos os trabalhos:\n{todos_os_trabalhos}")        
        return todos_os_trabalhos


    except Exception as e:
        print(f"Ocorreu algum problema como navegador {e}")

    finally:
        if driver:
            driver.quit()
            print("Driver fechado.")
# ---
def analisar_genero_primeiro_autor(trabalhos_coletados):
    """
    Processa os dados e retorna listas separadas,
    todas com o MESMO TAMANHO para o Pandas funcionar.
    """
    print("\n--- Iniciando Análise de Gênero (Primeiro Autor) ---")
    
    total_mulheres_primeira_autora = 0
    total_com_autores = 0 
    
    # Listas de retorno
    lista_titulos = []
    lista_primeiros_autores = []
    lista_generos = []
    lista_todos_autores = []
    lista_links = []

    for trabalho in trabalhos_coletados:
        
        # Adiciona os dados que sempre existem (Garante o alinhamento)
        lista_titulos.append(trabalho.get('titulo', 'N/A'))
        lista_links.append(trabalho.get('link', 'N/A'))
        
        autores = trabalho.get('autores', [])
        
        # Junta os autores em uma string (ex: "Nome1; Nome2")
        lista_todos_autores.append("; ".join(autores)) 
        
        if autores: # Se a lista de autores não estiver vazia
            total_com_autores +=1
            nome_completo_primeiro_autor = autores[0]
            partes_do_nome = nome_completo_primeiro_autor.split()
            
            # Adiciona o primeiro autor à lista
            lista_primeiros_autores.append(nome_completo_primeiro_autor)
            
            if partes_do_nome: 
                primeiro_nome = partes_do_nome[0]
                genero = br_gender_info.get_gender(primeiro_nome) 
                
                if genero == 'female' or genero == 'mostly_female':
                    status = "Feminino"
                    total_mulheres_primeira_autora += 1
                elif genero == 'male' or genero == 'mostly_male':
                    status = "Masculino"
                else:
                    status = "Indefinido" 

                lista_generos.append(status) # Adiciona o status à lista
                print(f"[ {status.ljust(10)} ] {nome_completo_primeiro_autor} - {trabalho['titulo'][:50]}...")
            
            else:
                print(f"[ {'N/A'.ljust(10)} ] (Nome inválido) - {trabalho['titulo'][:50]}...")
                lista_generos.append("N/A") # Mantém o alinhamento
        
        else: # Se 'autores' estiver vazio
            print(f"[ {'N/A'.ljust(10)} ] (Sem autores) - {trabalho['titulo'][:50]}...")
            # ADICIONA "N/A" PARA MANTER O ALINHAMENTO DAS LISTAS
            lista_primeiros_autores.append("N/A")
            lista_generos.append("N/A")

    print("--------------------------------------------------")
    print(f"Total de trabalhos raspados: {len(trabalhos_coletados)}")
    print(f"Total de trabalhos com autores: {total_com_autores}")
    print(f"Análise Concluída: {total_mulheres_primeira_autora} de {total_com_autores} trabalhos (com autores) têm uma mulher como primeira autora.")
    
    # Retorna todas as listas alinhadas
    return lista_titulos, lista_primeiros_autores, lista_generos, lista_todos_autores, lista_links


def monta_planilha(titulos, primeiros_autores, generos, todos_autores, links):
    """
    Recebe as listas alinhadas e cria o DataFrame.
    """
    print("\n--- Gerando planilha Excel ---")
    try:
        df_final = pd.DataFrame()
        # Cria as colunas com as listas
        df_final["Título"] = titulos
        df_final["Primeiro Autor"] = primeiros_autores
        df_final["Gênero (1º Autor)"] = generos
        df_final["Todos os Autores"] = todos_autores
        df_final["Link"] = links

        # Adiciona o nome do arquivo e remove o índice
        df_final.to_excel("/home/cayoalencar/Documentos/automacaoyasmin/relatorio_artigos.xlsx", index=False)
        print("Planilha 'relatorio_artigos.xlsx' salva com sucesso!")

    except ValueError as e:
        print(f"ERRO CRÍTICO AO GERAR PLANILHA: {e}")
        print("Isso geralmente significa que as listas não têm o mesmo tamanho.")
        # Imprime os tamanhos para depuração
        print(f"Tamanhos: Títulos={len(titulos)}, PrimeirosAutores={len(primeiros_autores)}, Gêneros={len(generos)}")
    
    except Exception as e:
        print(f"Erro ao salvar planilha: {e}")
        print("Verifique se você tem o 'openpyxl' instalado: pip install openpyxl")

if __name__ == "__main__":
    
    url_alvo1 = "https://www.even3.com.br/anais/iii-eneci-383547/"
    url_alvo2 = "https://www.even3.com.br/anais/eneci2020/"
    url_alvo3 = "https://sites.usp.br/lapef/eneci/anais/"
    
    all_jobs = []
    
    # 1. Roda o scraping do Even3
    for url_alvo in [url_alvo1, url_alvo2]:
        trabalhos_encontrados_even3 = scrape_trabalhos(url_alvo)
        all_jobs.extend(trabalhos_encontrados_even3)

    # 2. Roda o scraping do LAFEF
    trabalhos_encontrados_lapef = scrape_lapef(url_alvo3)
    all_jobs.extend(trabalhos_encontrados_lapef)


    if all_jobs:
        # 3. CAPTURA os resultados da análise
        titulos, primeiros_autores, generos, todos_autores, links = analisar_genero_primeiro_autor(all_jobs)
        
        # 4. PASSA os resultados para montar a planilha
        monta_planilha(titulos, primeiros_autores, generos, todos_autores, links)
    else:
        print("Nenhum trabalho encontrado.")