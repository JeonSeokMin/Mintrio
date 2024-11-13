import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def crawling(url, start_page=1, end_page=3):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 2000)")
    driver.implicitly_wait(5)

    # 결과를 저장할 딕셔너리 초기화
    res_dict = {
        "reviewer": [],
        "rating": [],
        "review": []
    }

    try:
        # "고객 리뷰" 버튼 클릭하여 리뷰 페이지로 이동
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'goods_reputation'))
        )
        review_button.click()
        time.sleep(2)  # 페이지 로딩 대기

        for page_num in range(start_page, end_page + 1):  # 지정한 페이지 범위에서만 크롤링
            # 각 리뷰의 컨테이너인 `review_cont` 요소들을 가져옴
            reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'review_cont'))
            )
            
            # `review_cont` 내부에서 작성자, 평점, 리뷰 텍스트를 개별적으로 추출
            for review in reviews:
                try:
                    # 작성자 정보 추출
                    reviewer = review.find_element(By.CLASS_NAME, 'id').text
                    # 평점 정보 추출
                    rating = review.find_element(By.CLASS_NAME, 'review_point').text
                    # 리뷰 텍스트 추출
                    review_text = review.find_element(By.CLASS_NAME, 'txt_inner').text

                    # 딕셔너리에 저장
                    res_dict["reviewer"].append(reviewer)
                    res_dict["rating"].append(rating)
                    res_dict["review"].append(review_text)
                except:
                    print("리뷰 데이터 일부를 가져오지 못했습니다.")
            
            # 다음 페이지로 이동
            if page_num < end_page:  # 마지막 페이지 전까지는 다음 페이지로 이동
                try:
                    # 페이지 번호를 통해 이동
                    page_link = driver.find_element(By.XPATH, f"//a[@data-page-no='{page_num + 1}']")
                    page_link.click()
                    time.sleep(2)  # 페이지 로딩 대기
                except Exception as e:
                    print(f"{page_num + 1} 페이지로 이동 중 오류 발생:", e)
                    break

    except Exception as e:
        print("오류 발생:", e)
    finally:
        driver.quit()

    return res_dict

# 실행 예제
if __name__ == "__main__":
    user_url = input("크롤링할 URL을 입력하세요: ")

    # 크롤링 실행 (예: 1~3 페이지만 크롤링)
    review_dict = crawling(user_url, start_page=1, end_page=3)
    review_df = pd.DataFrame(review_dict)

    # 결과를 엑셀 파일로 저장
    review_df.to_excel('revuewxusx/review_data.xlsx', index=False, engine='openpyxl')
    print("크롤링된 데이터가 review_data.xlsx 파일로 저장되었습니다.")
