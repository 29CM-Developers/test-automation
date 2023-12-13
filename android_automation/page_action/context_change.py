from time import sleep


def switch_context(wd, context):
    native = wd.contexts[0]
    webview = wd.contexts[-1]
    if context == 'native':
        wd.switch_to.context(native)
    elif context == 'webview':
        wd.switch_to.context(webview)
    print(f'{wd.current_context} 전환 완료')


def change_webview_contexts(wd):
    # 앱에서 웹뷰로 전환
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)
    # 웹뷰로 전환
    wd.switch_to.context(webview_contexts[-1])  # 가장 최근의 웹뷰 컨텍스트로 전환
    print(f'wd.current_window_handle : {wd.current_window_handle}')
    print(f'wd.window_handles : {wd.window_handles}')
    print("웹뷰로 전환 성공")
    sleep(4)


def change_native_contexts(wd):
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)
    # 네이티브로 전환
    wd.switch_to.context('NATIVE_APP')
    print("네이티브 변환 성공")
