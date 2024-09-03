import os
import pandas as pd

# CSV 파일들이 있는 기본 디렉토리 경로
base_dir = "./product_data"

all_data = []

# 디렉토리를 순회하며 CSV 파일을 읽어 리스트에 저장
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            data = pd.read_csv(file_path)
            data['source_file'] = file  # 원본 파일명을 열에 추가하여 구분 가능하게 함
            all_data.append(data)

# 모든 데이터를 하나의 데이터프레임으로 합침
combined_data = pd.concat(all_data, ignore_index=True)

# 합쳐진 데이터를 새로운 CSV 파일로 저장
output_file = "./merged_product_data.csv"
combined_data.to_csv(output_file, index=False)

print(f"CSV 파일들이 성공적으로 합쳐졌습니다: {output_file}")
