from time import time
from com_utils.testrail_api import send_test_result
from com_utils import values_control
from com_utils.db_connection import connect_db, insert_data, disconnect_db


def finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title):
    """
    finally optimization
    1. run file setUp에 self.user 변수가 필요합니다.
       기본은 'pipeline'으로 설정해주시고 local 실행 시 DB적재를 하지 않기 위해 'local'로 값을 변경해주세요
    2. testcase_title에는 testrail에 등록되어있는 테스트자동화 case의 title을 포함해주시면 됩니다. (기존에는 하드코딩 되어있었음)
    """
    run_time = f"{time() - start_time:.2f}"
    result_data = {
        'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
        'test_name': test_name, 'run_time': run_time}
    if self.user == 'pipeline':
        send_test_result(self, test_result, testcase_title)
        connection, cursor = connect_db(self)
        insert_data(connection, cursor, self, result_data)
        disconnect_db(connection, cursor)
    return result_data


def exception_control(wd, sys, os, traceback, error_texts=[]):
    test_result = 'FAIL'
    wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
    img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
    error_text = traceback.format_exc().split('\n')
    try:
        error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
        error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
        error_texts.append(values_control.find_next_value(error_text, 'Exception'))
    except Exception:
        pass

    return test_result, img_src, error_texts