import requests
import zipfile
import io

def get_repo_list(username, page):
    per_page = 100  # Número máximo de repositórios por página (limite da API)
    url = f"https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}"
    response = requests.get(url)
    repos = response.json()
    return repos

def download_repo(repo_name, download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(repo_name + ".zip", 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Repositório '{repo_name}' baixado com sucesso.")

        # Descompacta o arquivo ZIP
        with zipfile.ZipFile(repo_name + ".zip", 'r') as zip_ref:
            zip_ref.extractall(repo_name)
        print(f"Repositório '{repo_name}' descompactado com sucesso.")
    else:
        print(f"Erro ao baixar o repositório '{repo_name}'. Status Code: {response.status_code}")

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
    print("3. Sair")

    choice = input("Escolha uma opção (1/2/3): ")

    if choice == '1':
        repo_number = input("Digite o número do repositório para baixar: ")
        try:
            repo_index = int(repo_number) - 1
            if 0 <= repo_index < len(repos):
                repo = repos[repo_index]
                repo_name = repo['name']
                repo_download_url = repo['clone_url'] + "/archive/master.zip"
                download_repo(repo_name, repo_download_url)
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
        break

    else:
        print("Opção inválida. Por favor, tente novamente.")
