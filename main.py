import os
from perfume import scrape_category
from categories import categories

def main():
    

    # 각 카테고리에 대해 크롤링을 실행하고 데이터를 저장합니다.
    for category in categories:
        # 디렉토리 경로를 카테고리 구조에 따라 유동적으로 생성
        directory_parts = [category['top_category_name'], category['middle_category_name'], category['bottom_category_name']]
        if category['sub_category_name']:
            directory_parts.append(category['sub_category_name'])

        directory_path = os.path.join(*directory_parts).replace(" ", "_")
        
        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(directory_path, exist_ok=True)
        
        # 파일 이름을 sub_category_name 또는 bottom_category_name으로 설정
        output_file = os.path.join(directory_path, f"{category['sub_category_name'] or category['bottom_category_name'].replace(' ', '_')}.csv")
        
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
