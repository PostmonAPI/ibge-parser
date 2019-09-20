import contextlib
import csv
import os
import shutil
import urllib.request

import requests_html
import xlrd

url = 'https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html'


def find_xls_link(response):
    links = response.html.find('#acesso-ao-produto a')
    xls_link = next(link for link in links if link.text == 'xls')
    assert xls_link

    return xls_link.attrs['href']



def ftp_download(url):
    _, filename = os.path.split(url)
    with contextlib.closing(urllib.request.urlopen(url)) as r:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r, f)

    return filename


def csv_from_excel(filename):
    wb = xlrd.open_workbook(filename)
    for sheet in wb.sheets():
        with open(f'data/{sheet.name}.csv', 'w') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)

            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)

                if not row[0]:
                    continue

                try:
                    row[0] = int(row[0])
                except ValueError:
                    pass


                wr.writerow(row)


def main():
    session = requests_html.HTMLSession()
    response = session.get(url)

    xls_link = find_xls_link(response)
    filename = ftp_download(xls_link)

    csv_from_excel(filename)


if __name__ == '__main__':
    main()
