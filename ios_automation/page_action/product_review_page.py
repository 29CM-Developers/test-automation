from selenium.common import NoSuchElementException

from com_utils.element_control import ialc, ial


def click_back_btn(wd):
    ialc(wd, 'back icon')


def check_no_reviews_available(wd):
    try:
        ial(wd, '아직 리뷰를 작성할 수 있는')
        ial(wd, '주문내역이 없습니다.')
        print("주문 건이 없을 경우, 상품 리뷰 확인 - 작성 가능 리뷰")
    except NoSuchElementException:
        print("주문 건이 없을 경우, 상품 리뷰 확인 실패 - 작성 가능 리뷰")
        raise Exception('주문 건이 없을 경우, 상품 리뷰 확인 실패')


def click_my_review_tab(wd):
    ialc(wd, '내 리뷰 (')


def check_no_written_reviews(wd):
    try:
        ial(wd, '작성한 리뷰가 없습니다.')
        print("주문 건이 없을 경우, 상품 리뷰 확인 - 내 리뷰")
    except NoSuchElementException:
        print("주문 건이 없을 경우, 상품 리뷰 확인 실패 - 내 리뷰")
        raise Exception('주문 건이 없을 경우, 상품 리뷰 확인 실패')
