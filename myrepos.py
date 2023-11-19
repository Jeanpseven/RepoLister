import requests
import subprocess
import os
import shutil
import sys

def get_repo_list(username, page):
    per_page = 100
    url = f"https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}"
    response = requests.get(url)
    repos = response.json()
    return repos

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

# Obtém a lista de repositórios do usuário
username = "Jeanpseven"
page = 1
repos = get_repo_list(username, page)

while True:
    # Exibe a lista numerada de repositórios
    print(f"Repositórios disponíveis para {username} (Página {page}):")
    for index, repo in enumerate(repos, start=1):
        print(f"{index}. {repo['name']}")

    print("\nOpções:")
    print("1. Baixar um repositório")
    print("2. Listar mais repositórios")
    print("3. Atualizar o script")
    print("4. Sair")

    choice = input("Escolha uma opção (1/2/3/4): ")

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
        page += 1
        repos = get_repo_list(username, page)
        if not repos:
            print("Não há mais repositórios disponíveis.")
            page -= 1

    elif choice == '3':
        update_script()

    elif choice == '4':
        break

    else:
        print("Opção inválida. Por favor, tente novamente.")