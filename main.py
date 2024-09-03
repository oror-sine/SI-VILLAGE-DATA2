import os
from perfume import scrape_category
# from beauty import beauty
from categories.액세서리 import 액세서리

def main():
    # 각 카테고리에 대해 크롤링을 실행하고 데이터를 저장합니다.
    # for category in beauty:
    for category in 액세서리:
        # 디렉토리 경로를 카테고리 구조에 따라 유동적으로 생성
        directory_parts = [
            category['top_category_name'].replace("/", "_"),
            category['middle_category_name'].replace("/", "_"),
            category['bottom_category_name'].replace("/", "_")
        ]
        if category['sub_category_name']:
            directory_parts.append(category['sub_category_name'].replace("/", "_"))

        # 마지막 부분을 파일 이름으로 추출하고, 디렉토리 경로에서 제거
        file_name_part = directory_parts.pop()  # 마지막 항목을 추출하여 파일 이름으로 사용
        directory_path = os.path.join(*directory_parts)
        
        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(directory_path, exist_ok=True)
        
        # 파일 이름을 설정 (파일 이름에서 `_`를 다시 `/`로 변경)
        file_name = file_name_part.replace('_', '_')
        output_file = os.path.join(directory_path, f"{file_name}.csv")
        
        print(f"Scraping category: {category['bottom_category_name']}")
        
        scrape_category(
            category_url=category['url'], 
            output_file=output_file,
            max_items=100, 
            top_category_name=category['top_category_name'], 
            middle_category_name=category['middle_category_name'], 
            bottom_category_name=category['bottom_category_name'],
            sub_category_name=category['sub_category_name']
        )
        
        print(f"Finished scraping category: {category['sub_category_name'] or category['bottom_category_name']}")

if __name__ == "__main__":
    main()
