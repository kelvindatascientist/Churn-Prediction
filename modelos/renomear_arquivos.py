import os

def renomear_arquivos(pasta, prefixo):
    for nome_arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, nome_arquivo)

        if os.path.isfile(caminho_completo):
            novo_nome = prefixo + nome_arquivo
            novo_caminho = os.path.join(pasta, novo_nome)
            os.rename(caminho_completo, novo_caminho)
            print(f"Renomeado: {nome_arquivo} -> {novo_nome}")

if __name__ == "__main__":
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    target_folder = os.path.join(pasta_atual, "dataset")
    prefixo_arquivo = "NOVO_"
    
    if not os.path.exists(target_folder):
        print(f"A pasta especificada não existe: {target_folder}")
    else:
        renomear_arquivos(target_folder, prefixo_arquivo)
