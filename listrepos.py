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
            zip_ref.extractall()
        print(f"Repositório '{repo_name}' descompactado com sucesso.")
    else:
        print(f"Erro ao baixar o repositório '{repo_name}'. Status Code: {response.status_code}")

while True:
    print("\nOpções:")
    print("1. Listar repositórios de um usuário")
    print("2. Baixar um repositório")
    print("3. Sair")

    choice = input("Escolha uma opção (1/2/3): ")

    if choice == '1':
        username = input("Digite o nome de usuário: ")
        page = 1
        repos = get_repo_list(username, page)

        while True:
            # Exibe a lista numerada de repositórios
            print(f"\nRepositórios disponíveis para {username} (Página {page}):")
            for index, repo in enumerate(repos, start=1):
                print(f"{index}. {username}/{repo['name']}")

            print("\nOpções:")
            print("1. Listar mais repositórios")
            print("2. Voltar")

            inner_choice = input("Escolha uma opção (1/2): ")

            if inner_choice == '1':
                page += 1
                repos = get_repo_list(username, page)
                if not repos:
                    print("Não há mais repositórios disponíveis.")
                    page -= 1

            elif inner_choice == '2':
                break

            else:
                print("Opção inválida. Por favor, tente novamente.")

    elif choice == '2':
        repo_name = input("Digite o nome do repositório: ")
        username = input("Digite o nome de usuário do repositório: ")
        repo_download_url = f"https://github.com/{username}/{repo_name}/archive/master.zip"
        download_repo(repo_name, repo_download_url)

    elif choice == '3':
        break

    else:
        print("Opção inválida. Por favor, tente novamente.")
