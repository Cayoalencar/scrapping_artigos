# Projeto de Scraping de Anais de Conferências

Este script em Python realiza web scraping de múltiplos anais de conferências (Even3 e LAFEF/USP) para extrair informações sobre trabalhos, títulos e autores.

Após a coleta, o script processa os dados para identificar o gênero do primeiro autor de cada trabalho e, ao final, compila todos os dados em uma única planilha Excel (`relatorio_artigos.xlsx`).

---

## 🛠️ Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

1.  **Python 3.8** (ou mais recente).
2.  **Git** (para clonar o repositório).
3.  **Google Chrome** (o navegador). O script depende dele para rodar.

---

## 🚀 Instruções de Instalação e Execução

O processo de configuração envolve clonar o projeto, criar um ambiente virtual (`venv`) e instalar as dependências a partir do arquivo `requirements.txt`.

### 🐧 No Linux (Ubuntu/Debian)

1.  **Instale o Google Chrome:**
    O `webdriver-manager` do Python controla o Chrome, mas não o instala. Você precisa do navegador no sistema:
    ```bash
    wget [https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)
    sudo apt install ./google-chrome-stable_current_amd64.deb -y
    ```

2.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

3.  **Crie e ative o Ambiente Virtual (venv):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *Seu terminal deve agora mostrar `(venv)` no início.*

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 🪟 No Windows

1.  **Instale o Google Chrome:**
    Se ainda não o tiver, baixe e instale o [Google Chrome](https://www.google.com/chrome/).

2.  **Clone o repositório:**
    Abra o `Git Bash` ou `PowerShell` e clone o projeto.
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

3.  **Crie e ative o Ambiente Virtual (venv):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    *Seu terminal deve agora mostrar `(venv)` no início.*

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚡ Como Rodar o Script

Após o `venv` estar ativado e as dependências instaladas, execute o script principal (vou chamá-lo de `nome.py`, mas ajuste se o seu tiver outro nome):

```bash
python nome.py
