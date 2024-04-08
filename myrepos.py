import requests
import subprocess
import os
import shutil
import sys

total_pages = 1  # Inicializa com 1 página
current_page = 1
historico_scripts = []  # Nova lista para armazenar scripts baixados

def get_repo_list(username):
    per_page = 100
    url = f"https://api.github.com/users/{username}/repos?page=1&per_page={per_page}"
    response = requests.get(url)
    repos = response.json()
    global total_pages
    total_repos = response.headers.get('link')
    if total_repos:
        total_pages = int(total_repos[total_repos.find('page=')+5:total_repos.find('>; rel="last"')])
    else:
        total_pages = 1
    return repos

def get_all_repos(username):
    all_repos = []
    for page in range(1, total_pages + 1):
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"
        response = requests.get(url)
        repos = response.json()
        all_repos.extend(repos)
    return all_repos

def download_repo(repo_name, clone_url):
    if os.path.exists(repo_name):
        try:
            # Remove o diretório existente antes de clonar
            print(f"Removendo diretório existente '{repo_name}'...")
            shutil.rmtree(repo_name)
        except Exception as e:
            print(f"Erro ao remover diretório '{repo_name}': {e}")

    # Agora, podemos prosseguir com o clone
    clone_command = f"git clone {clone_url} {repo_name}"
    try:
        subprocess.run(clone_command, shell=True, check=True)
        print(f"Repositório '{repo_name}' clonado com sucesso.")
        historico_scripts.append(repo_name)  # Adiciona ao histórico de scripts
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o repositório '{repo_name}'. Código de erro: {e.returncode}")

def update_script():
    try:
        print("Atualizando o script...")
        subprocess.run("git pull", shell=True, check=True)
        print("Script atualizado com sucesso.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar o script. Código de erro: {e.returncode}")
        sys.exit(1)

def search_repos(repos, search_query):
    results = []
    for repo in repos:
        if search_query.lower() in repo['name'].lower():
            results.append(repo)
        else:
            # Se o termo de pesquisa não estiver no nome do repositório,
            # vamos buscar no conteúdo do README.md
            readme_url = f"https://raw.githubusercontent.com/{repo['full_name']}/master/README.md"
            readme_response = requests.get(readme_url)
            if readme_response.status_code == 200:
                readme_content = readme_response.text.lower()
                if search_query.lower() in readme_content:
                    results.append(repo)
    return results

# Obtém a lista de repositórios do usuário
username = "Jeanpseven"
repos = get_repo_list(username)

while True:
    # Exibe a lista numerada de repositórios
    print(f"Repositórios disponíveis para {username} (Página {current_page}/{total_pages}):")
    for index, repo in enumerate(repos, start=1):
        print(f"{index}. {repo['name']}")

    print("\nOpções:")
    print("1. Baixar um repositório")
    print("2. Listar mais repositórios")
    print("3. Pesquisar repositórios")
    print("4. Atualizar o script")
    print("5. Sair")

    choice = input("Escolha uma opção (1/2/3/4/5): ")

    if choice == '1':
        repo_number = input("Digite o número do repositório para baixar: ")
        try:
            repo_index = int(repo_number) - 1
            if 0 <= repo_index < len(repos):
                repo = repos[repo_index]
                repo_name = repo['name']
                repo_clone_url = repo['clone_url']
                download_repo(repo_name, repo_clone_url)
            else:
                print("Número de repositório inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    elif choice == '2':
        if current_page < total_pages:
            current_page += 1
            repos = get_all_repos(username)
        else:
            print("Não há mais repositórios disponíveis.")

    elif choice == '3':
        search_query = input("Digite o termo de pesquisa: ")
        search_results = search_repos(repos, search_query)
        if search_results:
            print("\nResultados da pesquisa:")
            for repo in search_results:
                print(f"- {repo['name']}")
        else:
            print("Nenhum resultado encontrado.")

    elif choice == '4':
        update_script()

    elif choice == '5':
        print("\nHistórico de Compras:")
        for script in historico_scripts:
            print(f"• {script}")

        print("\nVolte sempre! Obrigado pela preferência.\n")
        sys.exit(0)

    else:
        print("Opção inválida. Por favor, tente novamente.")