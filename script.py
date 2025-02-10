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
    """Baixa o feed XML compactado e retorna os dados brutos."""
    response = requests.get(url, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Erro ao baixar o feed! Código HTTP: {response.status_code}")
        exit(1)

    print(f"✅ Feed baixado com sucesso! Tamanho: {len(response.content)} bytes")
    return response.content

def descompactar_xml(dados_compactados):
    """Descompacta os dados do arquivo .gz e retorna o XML como string."""
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(dados_compactados)) as f:
            xml_data = f.read().decode("utf-8")
        print(f"✅ XML descompactado! Tamanho: {len(xml_data)} caracteres")
        return xml_data
    except Exception as e:
        print(f"❌ Erro ao descompactar o XML: {e}")
        exit(1)

def converter_xml_para_json(xml_data):
    """Converte o XML para JSON, extraindo apenas os campos necessários."""
    try:
        root = ET.fromstring(xml_data)
        vagas = []

        for job in root.findall("job"):
            vaga = {
                "titulo": job.findtext("title", "").strip(),
                "descricao": job.findtext("description", "").strip(),
                "url": job.findtext("urlDeeplink", "").strip(),
                "empresa": job.find("company/name").text if job.find("company/name") is not None else "",
                "localizacao": job.find("locations/location/state").text if job.find("locations/location/state") is not None else "",
            }
            vagas.append(vaga)

        print(f"✅ Extração concluída! Total de vagas: {len(vagas)}")
        return vagas

    except ET.ParseError as e:
        print(f"❌ Erro ao processar o XML: {e}")
        exit(1)

def salvar_json(dados, arquivo):
    """Salva os dados extraídos em um arquivo JSON."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"✅ JSON salvo com sucesso: {arquivo}")

# 🏁 Fluxo principal do script
if __name__ == "__main__":
    xml_bruto = baixar_feed(FEED_URL)
    xml_texto = descompactar_xml(xml_bruto)
    vagas_extraidas = converter_xml_para_json(xml_texto)
    salvar_json(vagas_extraidas, JSON_FILE)
