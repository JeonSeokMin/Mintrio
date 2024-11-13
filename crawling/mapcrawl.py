# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import time

# # 사용자로부터 링크 입력
# SEARCH = input("검색할 구글 지도 링크를 입력하세요: ")

# # 브라우저 꺼짐 방지 옵션 설정
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 로그 메시지 숨기기
# chrome_options.add_argument('disable-gpu')  # GPU 비활성화

# driver = webdriver.Chrome(options=chrome_options)
# driver.get(SEARCH)

# # 리뷰 데이터를 저장할 리스트
# reviews_list = []

# def main_search(driver):
#     # 페이지 로딩을 위한 대기
#     time.sleep(2)
    
#     # 스크롤을 내려 모든 리뷰가 로드될 수 있도록 시도
#     for _ in range(5):  # 스크롤을 여러 번 내려서 추가 리뷰 로드
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
    
#     # 리뷰가 포함된 요소가 로드될 때까지 대기 (리뷰의 고유 클래스를 사용)
#     try:
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.wiI7pd'))
#         )
#     except:
#         print("리뷰 요소를 찾지 못했습니다.")
#         return

#     # 리뷰 크롤링 로직
#     reviews = driver.find_elements(By.CSS_SELECTOR, '.wiI7pd')  # 리뷰 텍스트만 포함하는 클래스 선택
#     for review in reviews:
#         review_text = review.text  # 각 리뷰 텍스트 가져오기
#         reviews_list.append(review_text)  # 리스트에 추가
#         print(review_text)  # 각 리뷰 텍스트 출력

# # 실행
# main_search(driver)

# # 크롤링한 리뷰 데이터를 DataFrame으로 변환 후 CSV 파일로 저장
# df = pd.DataFrame(reviews_list, columns=["Review"])
# df.to_csv("mapriviews/google_map_reviews.csv", index=False, encoding="utf-8-sig")
# print("리뷰가 CSV 파일로 저장되었습니다.")


# crawl/mapscrawl.py
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class GoogleMaps:
    def __init__(self, url: str):
        self.url = url
        self.reviews_list = []
        
        # 브라우저 옵션 설정
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument('disable-gpu')
        
        # Chrome WebDriver 초기화
        self.driver = webdriver.Chrome(options=chrome_options)

    def start(self):
        """ Google Maps 페이지를 열고 리뷰 크롤링을 시작합니다. """
        self.driver.get(self.url)
        time.sleep(2)  # 페이지 로딩 대기
        self._scroll_and_load_reviews()
        self._scrape_reviews()
        self._save_to_excel()
        self.driver.quit()  # 크롤링 후 브라우저 종료

    def _scroll_and_load_reviews(self):
        """ 리뷰가 모두 로드될 수 있도록 페이지를 스크롤합니다. """
        for _ in range(5):  # 스크롤을 여러 번 내려서 추가 리뷰 로드
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    def _scrape_reviews(self):
        """ 스크롤 후 로드된 리뷰를 크롤링하여 리스트에 저장합니다. """
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.wiI7pd'))
            )
        except:
            print("리뷰 요소를 찾지 못했습니다.")
            return

        reviews = self.driver.find_elements(By.CSS_SELECTOR, '.wiI7pd')
        for review in reviews:
            review_text = review.text
            self.reviews_list.append(review_text)
            print(review_text)  # 각 리뷰 텍스트 출력

    def _save_to_excel(self):
        """ 크롤링한 리뷰 데이터를 Excel 파일로 저장합니다. """
        df = pd.DataFrame(self.reviews_list, columns=["Review"])
        
        # 저장할 디렉토리가 없으면 생성
        output_dir = "mapreviews"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Excel 파일로 저장 (encoding 옵션 제거)
        output_path = os.path.join(output_dir, "reviewxisxp.xlsx")
        df.to_excel(output_path, index=False)  # encoding 옵션 제거
        print("리뷰가 Excel 파일로 저장되었습니다.")
