import requests
import gzip
import xml.etree.ElementTree as ET
import json

# URL do feed XML compactado
FEED_URL = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Baixar e descompactar o XML
response = requests.get(FEED_URL)
if response.status_code == 200:
    xml_data = gzip.decompress(response.content)
else:
    print("Erro ao baixar o feed XML:", response.status_code)
    exit()

# Parse do XML
root = ET.fromstring(xml_data)

# Extrair dados relevantes
vagas = []
for job in root.findall("job"):
    vaga = {
        "titulo": job.find("title").text if job.find("title") is not None else "",
        "descricao": job.find("description").text if job.find("description") is not None else "",
        "url": job.find("urlDeeplink").text if job.find("urlDeeplink") is not None else "",
        "empresa": job.find("company/name").text if job.find("company/name") is not None else "",
        "localizacao": job.find("locations/location/state").text if job.find("locations/location/state") is not None else "",
    }
    vagas.append(vaga)

# Salvar como JSON
with open("vagas.json", "w", encoding="utf-8") as f:
    json.dump(vagas, f, ensure_ascii=False, indent=4)

print("Arquivo JSON gerado com sucesso!")
