import xml.etree.ElementTree as ET

def read_xml(xml_file):
  tree = ET.parse(xml_file)
  root = tree.getroot()
  table_name = root.attrib.get("nome")
  result = {
    "table_name": table_name,
    "columns": [],
    "pks": []
  }

  columns = root.find("colunas")
  pks = root.find("chaveprimaria").find("colunas")

  for column in columns:
    result["columns"].append({
      "name": column.attrib.get("nome"),
      "type": column.attrib.get("tipo"),
      "nullable": column.attrib.get("null"),
      "size": column.attrib.get("tamanho")
    })

  for pk in pks:
    result["pks"].append(pk.text)

  return result