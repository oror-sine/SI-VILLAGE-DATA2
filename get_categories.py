import os
import requests
from bs4 import BeautifulSoup


def get_categories():
    url = "https://www.sivillage.com/main/initMain.siv"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    top_categories = soup.select("div.nav__item > a")[1:]  # brand AtoZ 제외

    categories = []
    for top_category in top_categories:
        disp_ctg_no = top_category.get("data-disp_ctg_no")
        disp_clss_cd = top_category.get("data-disp_clss_cd")
        categories.extend(get_sub_categories(disp_ctg_no, disp_clss_cd))
        
    print(f"총 카테고리 수: {len(categories)}")
    
    with open('categories.py', 'w', encoding='utf-8') as f:
        f.write(f"categories={categories}")


def get_sub_categories(top_ctg_no, disp_clss_cd):
    url = f"https://www.sivillage.com/dispctg/initDispCtg.siv?disp_ctg_no={top_ctg_no}{f'&&disp_clss_cd={disp_clss_cd}'if disp_clss_cd else ''}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    top_category = soup.select_one("h2.lnb_menu__title")
    top_category_name = top_category and top_category.text

    categories = []

    for big in soup.select("ul.list-big > li"):
        middle_category = big.select_one("a")
        middle_category_name = middle_category and middle_category.text

        for medium in big.select("ul.list-medium > li"):
            bottom_category = medium.select_one("a")
            bottom_category_name = bottom_category and bottom_category.text

            tmp = []

            for small in big.select("ul.list-small > li"):
                sub_category = small.select_one("a")
                sub_category_name = sub_category and sub_category.text
                disp_ctg_no = sub_category and sub_category.get("data-disp_ctg_no")
                tmp.append(
                    {
                        "top_category_name": top_category_name,
                        "middle_category_name": middle_category_name,
                        "bottom_category_name": bottom_category_name,
                        "sub_category_name": sub_category_name,
                        "url": f"https://m.sivillage.com/dispctg/initDispCtg.siv?disp_ctg_no={disp_ctg_no}&outlet_yn=N",
                    }
                )

            if not tmp:
                disp_ctg_no = bottom_category and bottom_category.get(
                    "data-disp_ctg_no"
                )
                tmp.append(
                    {
                        "top_category_name": top_category_name,
                        "middle_category_name": middle_category_name,
                        "bottom_category_name": bottom_category_name,
                        "sub_category_name": None,
                        "url": f"https://m.sivillage.com/dispctg/initDispCtg.siv?disp_ctg_no={disp_ctg_no}&outlet_yn=N",
                    }
                )

            categories.extend(tmp)

    if not os.path.exists("./categories"):
        os.mkdir("./categories")

    trimed_top_category_name = top_category and top_category.text.replace("/", "_")

    with open(
        f"./categories/{trimed_top_category_name}.py", "w", encoding="utf-8"
    ) as f:
        f.write(f"{trimed_top_category_name}={categories}")

    return categories


if __name__ == "__main__":
    get_categories()
