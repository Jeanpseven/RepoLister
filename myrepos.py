import requests
import subprocess
import os
import shutil
import sys

def get_repo_list(username, page=1):
    per_page = 100
    url = f"https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}"
    response = requests.get(url)
    repos = response.json()
    total_pages = 1
    link_header = response.headers.get('link')
    if link_header:
        links = link_header.split(',')
        for link in links:
            if 'rel="last"' in link:
                total_pages = int(link[link.find('page=')+5:link.find('&')])
    return repos, total_pages

def download_repo(username, repo_name, clone_url):
    if os.path.exists(repo_name):
        try:
            print(f"Removendo diretório existente '{repo_name}'...")
            shutil.rmtree(repo_name)
        except Exception as e:
            print(f"Erro ao remover diretório '{repo_name}': {e}")

    clone_command = f"git clone {clone_url} {repo_name}"
    try:
        subprocess.run(clone_command, shell=True, check=True)
        print(f"Repositório '{repo_name}' clonado com sucesso.")
        return get_repo_list(username)  # Retorna para a função get_repo_list
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o repositório '{repo_name}'. Código de erro: {e.returncode}")
        return None, 0

def update_script(username):
    try:
        print("Atualizando o script...")
        subprocess.run("git pull", shell=True, check=True)
        print("Script atualizado com sucesso.")
        return get_repo_list(username)  # Retorna para a função get_repo_list
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar o script. Código de erro: {e.returncode}")
        return None, 0

def search_repos(repos, search_query):
    results = []
    for repo in repos:
        if search_query.lower() in repo['name'].lower():
            results.append(repo)
        else:
            readme_url = f"https://raw.githubusercontent.com/{repo['full_name']}/master/README.md"
            readme_response = requests.get(readme_url)
            if readme_response.status_code == 200:
                readme_content = readme_response.text.lower()
                if search_query.lower() in readme_content:
                    results.append(repo)
    return results

username = "Jeanpseven"
repos, total_pages = get_repo_list(username)

while True:
    print(f"Repositórios disponíveis para {username} (Página 1/{total_pages}):")
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
                repos, total_pages = download_repo(username, repo_name, repo_clone_url)
            else:
                print("Número de repositório inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    elif choice == '2':
        page = len(repos) // 100 + 1  # Calcula a próxima página
        if page <= total_pages:
            repos, total_pages = get_repo_list(username, page)
        else:
            print("Não há mais repositórios disponíveis.")

    elif choice == '3':
        search_query = input("Digite o termo de pesquisa: ")
        search_results = search_repos(repos, search_query)
        if search_results:
            print("\nResultados da pesquisa:")
            for index, repo in enumerate(search_results, start=1):
                print(f"{index}. {repo['name']}")
        else:
            print("Nenhum resultado encontrado.")

    elif choice == '4':
        repos, total_pages = update_script(username)

    elif choice == '5':
        print("""
        Histórico de Compras:
        """)
        for script in historico_scripts:
            print(f"• {script}")
        print("""Volte Sempre! Obrigado pela preferência
⠀⠈⢻⣆⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡏⠉⠉⠉⠉⢹⡏⠉⠉⠉⠉⣿⠉⠉⠉⠉⠉⣹⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣿⣀⣀⣀⣀⣸⣧⣀⣀⣀⣀⣿⣄⣀⣀⣀⣠⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⢠⡿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣷⠤⠼⠷⠤⠤⠤⠤⠿⠦⠤⠾⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢾⣷⢶⣶⠶⠶⠶⠶⠶⣶⠶⣶⡶⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣧⣠⡿⠀⠀⠀⠀⠀⠀⢷⣄⣼⠇⠀⠀
""")
        sys.exit(0)