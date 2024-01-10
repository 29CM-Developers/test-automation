from time import sleep

from com_utils.element_control import aal, aalc


def click_back_btn(wd):
    # 뒤로가기로 마이페이지 진입 확인
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    sleep(1)


def check_no_reviews_available(wd):
    sleep(1)
    review_guide = aal(wd, 'c_아직 리뷰를 작성할 수 있는\n주문내역이 없습니다.').text
    print(f"review_guide : {review_guide}")
    if review_guide == '아직 리뷰를 작성할 수 있는\n주문내역이 없습니다.':
        print("주문 건이 없을 경우, 상품 리뷰 없음 확인")
    else:
        print("주문 건이 없을 경우, 상품 리뷰 없음 확인 실패")
        raise Exception('주문 건이 없을 경우, 상품 리뷰 확인 실패')


def click_my_review_tab(wd):
    aalc(wd, 'c_내 리뷰 (')


def check_no_written_reviews(wd):
    my_review_guide = aal(wd, 'c_작성한 리뷰가 없습니다.').text
    print(f"my_review_guide : {my_review_guide}")
    if my_review_guide == '작성한 리뷰가 없습니다.':
        print("주문 건이 없을 경우, 상품 리뷰 없음 확인")
    else:
        print("주문 건이 없을 경우, 상품 리뷰 없음 확인 실패")
        raise Exception('주문 건이 없을 경우, 상품 리뷰 확인 실패')
