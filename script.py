import requests
import gzip
import xml.etree.ElementTree as ET
import json

# URL do feed XML comprimido
FEED_URL = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Estados que você deseja filtrar
ESTADOS_DESEJADOS = ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia"]

def baixar_feed():
    """Baixa e descompacta o feed XML."""
    resposta = requests.get(FEED_URL)
    with open("feed.xml.gz", "wb") as f:
        f.write(resposta.content)

    # Descompactar o XML
    with gzip.open("feed.xml.gz", "rb") as f_in:
        with open("feed.xml", "wb") as f_out:
            f_out.write(f_in.read())

def processar_xml():
    """Processa o XML e salva apenas os dados necessários em JSON."""
    tree = ET.parse("feed.xml")
    root = tree.getroot()

    vagas_filtradas = []

    for job in root.findall("job"):
        state = job.find("./locations/location/state")
        city = job.find("./locations/location/city")

        if state is not None and state.text in ESTADOS_DESEJADOS:
            vaga = {
                "title": job.find("title").text.strip(),
                "description": job.find("description").text.strip(),
                "url": job.find("urlDeeplink").text.strip(),
                "company": job.find("./company/name").text.strip(),
                "state": state.text.strip(),
                "city": city.text.strip() if city is not None else ""
            }
            vagas_filtradas.append(vaga)

    # Salvar em JSON
    with open("vagas.json", "w", encoding="utf-8") as f:
        json.dump(vagas_filtradas, f, ensure_ascii=False, indent=2)

# Executar o processo
baixar_feed()
processar_xml()
