# -*- coding: utf-8 -*-
"""캡스톤의약품API.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11fJZ9-qWjwQrImsNESPIPohW5EFVz56U
"""

import requests

# 첫 번째 API 요청(e약은요)
url1 = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
params1 = {
    'serviceKey': 'ReUuFpVLqmLES+zhaBZplcThd/fkf5H/bm6h78mYGc1yAF1QrlDoGjTYjHe6yfaetAA4+0npenXdVbNs6i3q8A==',
    'pageNo': '1',
    'numOfRows': '100',
    'type': 'xml'  # XML 형식으로 요청
}

response1 = requests.get(url1, params=params1)
# 첫 번째 API 응답 처리
if response1.status_code == 200:
    data1 = response1.text  # XML 형식의 데이터를 문자열로 받기
    print("첫 번째 API 데이터:")
    print(data1)
else:
    print("첫 번째 API 요청 실패:", response1.status_code)

import requests

# 두 번째 API 요청(의약품 낱알식별정)
url2 = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01"
params2 = {
    'serviceKey': 'yPzgaEXmWrDivZb/5pDombrZgY7nTlpMAgKIZdaJI2grK9OW5oxNmouDWVGyp+k0TIPHugj01BSPrbGO+PjC8A==',
    'pageNo': '1',
    'numOfRows': '100'
}

response2 = requests.get(url2, params=params2)

# 두 번째 API 응답 처리
if response2.status_code == 200:
    data2 = response2.text  # XML 형식의 데이터를 문자열로 받기
    print("두 번째 API 데이터:")
    print(data2)
else:
    print("두 번째 API 요청 실패:", response2.status_code)

"""e약은요

"""

import requests
import xml.etree.ElementTree as ET
import csv

# 이전에 저장된 데이터를 읽어와서 메모리에 저장하는 함수
def load_existing_data(filename):
    existing_data = set()  # 중복을 확인하기 위해 집합(set)을 사용
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 중복된 데이터는 품목 기준 코드로 판단
                existing_data.add(row['품목기준코드'])
    except FileNotFoundError:
        pass  # 파일이 없으면 빈 집합으로 유지
    return existing_data

# API 요청 설정
url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
params = {
    'serviceKey': 'ReUuFpVLqmLES+zhaBZplcThd/fkf5H/bm6h78mYGc1yAF1QrlDoGjTYjHe6yfaetAA4+0npenXdVbNs6i3q8A==',
    'numOfRows': '100',  # 한 페이지당 가져올 항목 수
    'type': 'xml'         # XML 형식으로 요청
}

# 이전에 저장된 데이터를 읽어와서 메모리에 저장
existing_data = load_existing_data('drug_data.csv')

# CSV 파일 열기
with open('drug_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
    # CSV writer 객체 생성
    fieldnames = ['품목기준코드', '제품명', '문항1', '문항2', '문항3', '문항4', '문항5', '문항6']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 최대한 많은 데이터를 가져오기 위해 반복
    while True:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            # XML 데이터 파싱
            root = ET.fromstring(response.content)
            items = root.findall('.//item')

            for item in items:
                itemSeq = item.find('itemSeq').text
                itemName = item.find('itemName').text

                # 중복된 데이터인지 확인
                if itemSeq not in existing_data:
                    efcyQesitm = item.find('efcyQesitm').text
                    useMethodQesitm = item.find('useMethodQesitm').text
                    atpnWarnQesitm = item.find('atpnWarnQesitm').text
                    atpnQesitm = item.find('atpnQesitm').text
                    intrcQesitm = item.find('intrcQesitm').text
                    seQesitm = item.find('seQesitm').text

                    # 새로운 데이터를 CSV 파일에 추가
                    writer.writerow({
                        '품목기준코드': itemSeq,
                        '제품명': itemName,
                        '문항1': efcyQesitm,
                        '문항2': useMethodQesitm,
                        '문항3': atpnWarnQesitm,
                        '문항4': atpnQesitm,
                        '문항5': intrcQesitm,
                        '문항6': seQesitm
                    })

                    # 새로운 데이터의 품목 기준 코드를 메모리에 추가
                    existing_data.add(itemSeq)

            # 현재 가져온 데이터 수 확인
            current_items = len(items)

            # 가져온 데이터 수가 한 페이지당 항목 수보다 적으면 데이터가 더 이상 없는 것으로 판단하여 반복문 종료
            if current_items < int(params['numOfRows']):
                break

            # 다음 페이지를 가져오기 위해 페이지 번호가 없으면 생성하고, 있는 경우에는 증가시킴
            if 'pageNo' in params:
                params['pageNo'] = str(int(params['pageNo']) + 1)
            else:
                params['pageNo'] = '2'  # 페이지 번호가 없는 경우에는 2로 설정
        else:
            print(f"API 요청 실패 - 페이지 {params.get('pageNo', '1')}: {response.status_code}")
            break

import csv

with open('drug_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

import csv

# 중복을 확인할 품목기준코드를 저장할 세트(set) 생성
itemSeq_set = set()

# 중복된 품목기준코드를 저장할 리스트 생성
duplicates = []

with open('drug_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 헤더 행은 건너뜁니다.
    for row in reader:
        itemSeq = row[0]  # 품목기준코드는 첫 번째 열에 위치한다고 가정합니다.
        # 이미 세트에 존재하는 경우 중복으로 판단하고 duplicates 리스트에 추가합니다.
        if itemSeq in itemSeq_set:
            duplicates.append(itemSeq)
        else:
            itemSeq_set.add(itemSeq)

# 중복된 품목기준코드 출력
print("중복된 품목기준코드:", duplicates)

import csv

# 중복을 확인할 품목기준코드를 저장할 세트(set) 생성
itemSeq_set = set()

# CSV 파일에서 품목기준코드의 총 개수를 세는 변수
total_itemSeq = 0

with open('drug_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 헤더 행은 건너뜁니다.
    for row in reader:
        itemSeq = row[0]  # 품목기준코드는 첫 번째 열에 위치한다고 가정합니다.
        # 중복을 체크하지 않고 모든 품목기준코드를 세기 때문에 중복 포함된 전체 개수가 됩니다.
        total_itemSeq += 1
        itemSeq_set.add(itemSeq)  # 세트에 품목기준코드를 추가합니다.

# 총 품목기준코드의 개수 출력
print("총 품목기준코드의 개수:", len(itemSeq_set))

import csv

# CSV 파일 열기
with open('drug_data.csv', 'r', encoding='utf-8') as csvfile:
    # CSV 리더 생성
    reader = csv.reader(csvfile)

    # 첫 번째 행을 읽어와서 파일 헤더를 확인
    header = next(reader)
    print("파일 헤더:", header)

import pandas as pd

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv('drug_data.csv')

# 열 이름을 포함한 첫 번째 행 지정
header = ['품목기준코드', '제품명', '문항1', '문항2', '문항3', '문항4', '문항5', '문항6']

# CSV 파일을 UTF-8 인코딩으로 다시 저장하여 다운로드
df.to_csv('drug_data_utf8.csv', encoding='utf-8-sig', index=False, header=header)

import csv

# CSV 파일 열기
with open('drug_data_utf8.csv', 'r', encoding='utf-8') as csvfile:
    # CSV 리더 생성
    reader = csv.reader(csvfile)

    # 첫 번째 행을 읽어와서 파일 헤더를 확인
    header = next(reader)
    print("파일 헤더:", header)











"""의약품 낱알식별 정보"""

import requests
import xml.etree.ElementTree as ET

def extract_medicine_data():
    url = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01"
    params = {
        "ServiceKey": "yPzgaEXmWrDivZb/5pDombrZgY7nTlpMAgKIZdaJI2grK9OW5oxNmouDWVGyp+k0TIPHugj01BSPrbGO+PjC8A==",
        "numOfRows": 100,  # 한 번에 가져올 항목 수
        "pageNo": 1,        # 페이지 번호
    }

    while True:
        response = requests.get(url, params=params)
        root = ET.fromstring(response.text)

        for item in root.findall('.//item'):
            item_seq = item.findtext('ITEM_SEQ')
            item_name = item.findtext('ITEM_NAME')
            item_image = item.findtext('ITEM_IMAGE')

            # 추출된 정보 출력 또는 저장
            print("ITEM_SEQ:", item_seq)
            print("ITEM_NAME:", item_name)
            print("ITEM_IMAGE:", item_image)
            print("=" * 50)

        # 다음 페이지 요청을 위해 페이지 번호 증가
        params['pageNo'] += 1

        # 마지막 페이지까지 데이터를 모두 추출한 경우 반복 종료
        if int(params['pageNo']) * int(params['numOfRows']) > int(root.findtext('.//totalCount')):
            break

# 데이터 추출 함수 호출
extract_medicine_data()

import requests
import csv
import xml.etree.ElementTree as ET

def load_existing_data(filename):
    existing_data = set()
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_data.add(row['ITEM_SEQ'])  # ITEM_SEQ를 중복 확인을 위한 기준으로 사용
    except FileNotFoundError:
        pass
    return existing_data

def extract_medicine_data_to_csv(filename):
    url = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01"
    params = {
        "ServiceKey": "yPzgaEXmWrDivZb/5pDombrZgY7nTlpMAgKIZdaJI2grK9OW5oxNmouDWVGyp+k0TIPHugj01BSPrbGO+PjC8A==",
        "numOfRows": 100,  # 한 번에 가져올 항목 수
        "pageNo": 1,        # 페이지 번호
    }

    # CSV 파일 열기 (이어쓰기 모드)
    with open(filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
        # CSV writer 객체 생성
        fieldnames = ['ITEM_SEQ', 'ITEM_NAME', 'ITEM_IMAGE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        existing_data = load_existing_data(filename)

        while True:
            response = requests.get(url, params=params)
            root = ET.fromstring(response.text)

            for item in root.findall('.//item'):
                item_seq = item.findtext('ITEM_SEQ')
                item_name = item.findtext('ITEM_NAME')
                item_image = item.findtext('ITEM_IMAGE')

                # 중복 확인
                if item_seq not in existing_data:
                    # 새로운 데이터를 CSV 파일에 추가
                    writer.writerow({'ITEM_SEQ': item_seq, 'ITEM_NAME': item_name, 'ITEM_IMAGE': item_image})
                    existing_data.add(item_seq)  # 중복을 피하기 위해 세트에 추가

            # 다음 페이지 요청을 위해 페이지 번호 증가
            params['pageNo'] += 1

            # 마지막 페이지까지 데이터를 모두 추출한 경우 반복 종료
            if int(params['pageNo']) * int(params['numOfRows']) > int(root.findtext('.//totalCount')):
                break

# 데이터를 CSV 파일에 저장
from google.colab import files
extract_medicine_data_to_csv('medicine_data.csv')

import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('medicine_data.csv')

# 처음 10줄의 데이터 출력
print(df.head(10))

from google.colab import drive
import pandas as pd

# 구글 드라이브 마운트
drive.mount('/content/drive')

# 구글 드라이브 경로 설정
file_path = '/content/drive/My Drive/의약품낱알.csv'

# CSV 파일을 DataFrame으로 읽어오기
df = pd.read_csv(file_path)

# ITEM_SEQ 열의 고유한 값 개수 확인
item_seq_count = df['ITEM_SEQ'].nunique()
print("ITEM_SEQ의 고유한 값 개수:", item_seq_count)

# 중복된 행 확인
duplicates = df[df.duplicated()]

if duplicates.empty:
    print("중복된 행이 없습니다.")
else:
    print("중복된 행이 있습니다.")



import requests
import xml.etree.ElementTree as ET

# 첫 번째 API 요청(e약은요)
url1 = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
params1 = {
    'serviceKey': 'ReUuFpVLqmLES+zhaBZplcThd/fkf5H/bm6h78mYGc1yAF1QrlDoGjTYjHe6yfaetAA4+0npenXdVbNs6i3q8A==',
    'pageNo': '1',
    'numOfRows': '100',
    'type': 'xml'  # XML 형식으로 요청
}

response1 = requests.get(url1, params=params1)

# 첫 번째 API 응답 처리
if response1.status_code == 200:
    # XML 데이터 파싱
    root = ET.fromstring(response1.content)

    # XML 데이터에서 필요한 컬럼 정보 추출
    columns = set()  # 중복을 허용하지 않는 데이터 구조인 set을 사용하여 컬럼명을 저장

    for item in root.iter('item'):
        for child in item:
            columns.add(child.tag)  # 태그명을 컬럼명으로 추가

    # 컬럼명 출력
    print("데이터 컬럼들:")
    for column in columns:
        print(column)

else:
    print("첫 번째 API 요청 실패:", response1.status_code)

import requests
import xml.etree.ElementTree as ET

# 두 번째 API 요청(의약품 낱알식별정)
url2 = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01"
params2 = {
    'serviceKey': 'yPzgaEXmWrDivZb/5pDombrZgY7nTlpMAgKIZdaJI2grK9OW5oxNmouDWVGyp+k0TIPHugj01BSPrbGO+PjC8A==',
    'pageNo': '1',
    'numOfRows': '100'
}

response2 = requests.get(url2, params=params2)

# 두 번째 API 응답 처리
if response2.status_code == 200:
    # XML 데이터 파싱
    root = ET.fromstring(response2.content)

    # XML 데이터에서 데이터 컬럼 정보 추출
    columns = set()  # 중복을 허용하지 않는 데이터 구조인 set을 사용하여 컬럼명을 저장

    # 첫 번째 item 요소의 자식 요소들을 컬럼으로 삼음
    first_item = root.find('.//item')  # 첫 번째 item 요소 찾기
    if first_item is not None:
        for child in first_item:
            columns.add(child.tag)  # 태그명을 컬럼명으로 추가

    # 컬럼명 출력
    print("두 번째 API 데이터 컬럼들:")
    for column in columns:
        print(column)

else:
    print("두 번째 API 요청 실패:", response2.status_code)

from google.colab import drive
import pandas as pd

# 구글 드라이브 마운트
drive.mount('/content/drive')

file2 = '/content/drive/My Drive/의약품낱알.csv'
df2 = pd.read_csv(file2)

file1 = '/content/drive/My Drive/e약은요.csv'
df1 = pd.read_csv(file1)

names1 = df1['품목기준코드']
names2 = df2['ITEM_SEQ']

duplicates = names1[names1.isin(names2)]
if not duplicates.empty:
  print(duplicates)
else:
  print('없음')

merged_df = pd.merge(df1, df2, how='inner', left_on='품목기준코드', right_on='ITEM_SEQ')
print(merged_df)

output_file_path = "/content/drive/My Drive/merged_data.csv"
merged_df.to_csv(output_file_path, index=False)

merged_df = pd.read_csv(output_file_path)
columns_list = merged_df.columns.tolist()
print(columns_list)

columns_to_drop = ['ITEM_SEQ', 'ITEM_NAME']
modified_df = merged_df.drop(columns=columns_to_drop)

print(modified_df)

modified_output_file_path = "/content/drive/My Drive/modified_merged_data.csv"
modified_df.to_csv(modified_output_file_path, index=False)

from google.colab import drive
drive.mount('/content/drive')

# 파일 경로
modified_output_file_path = "/content/drive/My Drive/modified_merged_data.csv"

# CSV 파일 읽기
modified_df = pd.read_csv(modified_output_file_path)

# 각 열의 문자열 길이 계산
max_lengths = modified_df.applymap(lambda x: len(str(x))).max()

# 가장 긴 문자열 길이와 해당 열 이름 찾기
longest_column_name = max_lengths.idxmax()
longest_string_length = max_lengths.max()

print(f"가장 긴 문자열의 길이: {longest_string_length}")
print(f"가장 긴 문자열을 포함한 열: {longest_column_name}")

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

file_path = "/content/drive/My Drive/질병 최종.csv"
df = pd.read_csv(file_path)

# 각 열의 문자열 길이 계산
max_lengths = df.applymap(lambda x: len(str(x))).max()

# 가장 긴 문자열 길이와 해당 열 이름 찾기
longest_column_name = max_lengths.idxmax()
longest_string_length = max_lengths.max()

print(f"가장 긴 문자열의 길이: {longest_string_length}")
print(f"가장 긴 문자열을 포함한 열: {longest_column_name}")

import pandas as pd

file_path = "/content/drive/My Drive/캡스톤DB/최종식품DB1.csv"
df = pd.read_csv(file_path)

# 각 열의 문자열 길이 계산
max_lengths = df.applymap(lambda x: len(str(x))).max()

# 가장 긴 문자열 길이와 해당 열 이름 찾기
longest_column_name = max_lengths.idxmax()
longest_string_length = max_lengths.max()

print(f"가장 긴 문자열의 길이: {longest_string_length}")
print(f"가장 긴 문자열을 포함한 열: {longest_column_name}")

import pandas as pd

file_path = "/content/drive/My Drive/식품DB_2.csv"
df = pd.read_csv(file_path)

# 각 열의 문자열 길이 계산
max_lengths = df.applymap(lambda x: len(str(x))).max()

# 가장 긴 문자열 길이와 해당 열 이름 찾기
longest_column_name = max_lengths.idxmax()
longest_string_length = max_lengths.max()

print(f"가장 긴 문자열의 길이: {longest_string_length}")
print(f"가장 긴 문자열을 포함한 열: {longest_column_name}")