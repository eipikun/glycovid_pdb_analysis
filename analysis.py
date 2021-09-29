import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
# PDBjに登録されているCOVID-19関連の構造をリスト化するスクレイピングプログラム
def get_pdbj_covid_19_structure_list():
    URI_PREFIX = 'https://pdbj.org/featured/covid-19?tab=all&page='
    result = []
    for _ in range(1, 60):
        res = requests.get(URI_PREFIX + str(_))
        soup = BeautifulSoup(res.text, 'html.parser')
        title_text = soup.find('tbody').find_all('a')
        for __ in range(len(title_text)):
            if '/mine/summary/' in title_text[__].get('href') and len(title_text[__].get_text()) == 4:
                result.append(title_text[__].get_text())
        time.sleep(1)

    df = pd.Series(result)
    df.to_csv('./pdbj_registered_covid19_structures.csv')

# PDBeから得たstructuresのcsvファイルを解析するプログラム
def categolize_by_label():

    FILE_PATHs = [
        "P0DTC1-coverage.csv",
        "P0DTC3-coverage.csv",
        "P0DTC4-coverage.csv",
        "P0DTC7-coverage.csv",
        "P0DTC8-coverage.csv",
        "P0DTC9-coverage.csv",
        "P0DTD1-coverage.csv",
        "P0DTD2-coverage.csv",
        "PRO_0000449619-coverage.csv",
        "PRO_0000449620-coverage.csv",
        "PRO_0000449621-coverage.csv",
        "PRO_0000449622-coverage.csv",
        "PRO_0000449623-coverage.csv",
        "PRO_0000449625-coverage.csv",
        "PRO_0000449626-coverage.csv",
        "PRO_0000449627-coverage.csv",
        "PRO_0000449628-coverage.csv",
        "PRO_0000449629-coverage.csv",
        "PRO_0000449630-coverage.csv",
        "PRO_0000449631-coverage.csv",
        "PRO_0000449632-coverage.csv",
        "PRO_0000449633-coverage.csv",
        "PRO_0000449649-coverage.csv"
    ]

    pd_files = []

    import pandas as pd

    for _ in range(len(FILE_PATHs)):
        data = pd.read_csv(r"./data/" + FILE_PATHs[_], header = 0)
        pd_files.append(data)

    pd_files = pd.concat(pd_files)
    # ラベルのみでグルーピングされたcsvの作成
    pd_files.groupby('label').count().to_csv('./data/label_grouped_structures.csv')
    # ラベルとアクセッションIDでグルーピングされたcsvの作成
    pd_files.groupby(['label','accession']).count().to_csv('./data/label_accession_grouped_structures.csv')

# PDBeとPDBjで取得された構造を比較し包含関係をまとめたファイルを出力するプログラム
def compare_pdbj_pdbe():
    array_pdbe = []
    array_pdbj = []
    import csv
    df = pd.read_csv(r"./data/label_grouped_structures.csv", header = 0)
    df[df['label'].str.len() == 4]['label'].str.upper().to_csv('./pdbe_registered_covid19_structures.csv')

    with open('./pdbe_registered_covid19_structures.csv') as f:
        for row in csv.reader(f):
            array_pdbe.append(row[1])

    with open('./pdbj_registered_covid19_structures.csv') as f:
        for row in csv.reader(f):
            array_pdbj.append(row[1])

    # pdbeにあって、pdbjにないモノ
    dict_pdbe_false = {}
    # pdbjにあって、pdbeにないモノ
    dict_pdbj_false = {}

    # PDBe・PDBj両方をまとめた辞書配列
    dict_inclusion = {}
    for pdbj in array_pdbj:
        if pdbj not in array_pdbe:
            dict_pdbj_false[pdbj] = True
            dict_inclusion[pdbj] = 'not in pdbe but in pdbj'
        else:
            dict_inclusion[pdbj] = 'in both pdbe and pdbj'

    for pdbe in array_pdbe:
        if pdbe not in array_pdbj:
            dict_pdbe_false[pdbe] = True
            dict_inclusion[pdbe] = 'not in pdbj but in pdbe'
        else:
            # find invalid value in dictionary
            if pdbe not in dict_inclusion:
                print(pdbe, 'ERROR')

    # OUTPUT option 1
    # PDBeとPDBjそれぞれで出力(dict_pdbj_false, dict_pdbe_falseはすでに上で作成済み)
    # filtered_pdbj_df = pd.DataFrame.from_dict(dict_pdbj_false, orient='index').rename(columns={0:'Non-exist'})
    # filtered_pdbe_df = pd.DataFrame.from_dict(dict_pdbe_false, orient='index').rename(columns={0:'Non-exist'})
    # filtered_pdbj_df.to_csv('./pdbj_inclusion.csv')
    # filtered_pdbe_df.to_csv('./pdbe_inclusion.csv')
    
    # OUTPUT option 2
    # PDBeとPDBjをまとめて出力
    dict_inclusion_upper = {}
    for k, v in dict_inclusion.items():
        dict_inclusion_upper[k.upper()] = v
    
    filtered_df = pd.DataFrame.from_dict(dict_inclusion_upper, orient='index').rename(columns={0:'Type'})
    filtered_df.to_csv('./pdbj_pdbe_relation.csv')

# PDBe・PDBjの持つ構造データ包含関係表示(compare_pdbj_pdbe関数にてoption2の出力データを準備しておく)
def static_pdbj_pdbe():
    df = pd.read_csv('./pdbj_pdbe_relation.csv')
    print(df.groupby('Type').count())

# get_pdbj_covid_19_structure_list()
# categolize_by_label()
# compare_pdbj_pdbe()
# static_pdbj_pdbe()