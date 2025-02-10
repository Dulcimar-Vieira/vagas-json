import requests
import gzip
import io
import xml.etree.ElementTree as ET
import json

# URL do feed XML
FEED_URL = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Nome do arquivo JSON de saída
JSON_FILE = "vagas.json"

def baixar_feed(url):
    """Baixa o feed XML compactado e retorna um objeto de fluxo de bytes."""
    response = requests.get(url, stream=True, timeout=60)
    
    if response.status_code != 200:
        print(f"❌ Erro ao baixar o feed! Código HTTP: {response.status_code}")
        exit(1)

    print("✅ Feed baixado com sucesso!")
    return io.BytesIO(response.content)

def extrair_vagas(xml_stream):
    """Lê o XML compactado e processa os dados sem carregar tudo na memória."""
    vagas = []
    
    with gzip.GzipFile(fileobj=xml_stream) as f:
        context = ET.iterparse(f, events=("start", "end"))
        _, root = next(context)  # Obtém o elemento raiz do XML

        for event, elem in context:
            if event == "end" and elem.tag == "job":
                vaga = {
                    "titulo": elem.findtext("title", "").strip(),
                    "descricao": elem.findtext("description", "").strip(),
                    "url": elem.findtext("urlDeeplink", "").strip(),
                    "empresa": elem.find("company/name").text if elem.find("company/name") is not None else "",
                    "localizacao": elem.find("locations/location/state").text if elem.find("locations/location/state") is not None else "",
                }
                vagas.append(vaga)

                # Libera memória removendo o elemento processado
                root.clear()

        print(f"✅ Extração concluída! Total de vagas: {len(vagas)}")
        return vagas

def salvar_json(dados, arquivo):
    """Salva os dados extraídos em um arquivo JSON."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"✅ JSON salvo com sucesso: {arquivo}")

# 🏁 Fluxo principal do script
if __name__ == "__main__":
    xml_stream = baixar_feed(FEED_URL)
    vagas_extraidas = extrair_vagas(xml_stream)
    salvar_json(vagas_extraidas, JSON_FILE)
