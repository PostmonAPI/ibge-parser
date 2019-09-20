import csv
import json


def _read(filename):
    data = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        data.extend(reader)

    return data


def ufs():
    for line in _read('data/AR_BR_UF_2018.csv'):
        yield {
            'sigla': line['NM_UF_SIGLA'],
            'codigo_ibge': line['CD_GCUF'],
            'nome': line['NM_UF'],
            'area_km2': line['AR_MUN_2018'],
        }


def municipios():
    for line in _read('data/AR_BR_MUN_2018.csv'):
        yield {
            'codigo_ibge_uf': line['CD_GCUF'],
            'sigla_uf': line['NM_UF_SIGLA'],
            'codigo_ibge': line['CD_GCMUN'],
            'nome': line['NM_MUN_2018'],
            'area_km2': line['AR_MUN_2018'],
        }


def main():
    with open('data/postmon-ufs.json', 'w') as f:
        json.dump(list(ufs()), f, indent=2)

    with open('data/postmon-municipios.json', 'w') as f:
        json.dump(list(municipios()), f, indent=2)


if __name__ == '__main__':
    main()
