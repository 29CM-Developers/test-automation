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
    # 현재 창의 핸들을 저장
    current_handle = wd.current_window_handle
    print(f'현재 핸들러 확인 : {wd.current_window_handle}')
    # 새로운 창이 열린 후의 창 핸들들을 가져오기
    window_handles = wd.window_handles
    print(f'전체 윈도우 핸들러 확인 : {window_handles}')
    # 새로 열린 창으로 전환
    for handle in reversed(window_handles):
        if handle != current_handle:
            wd.switch_to.window(handle)
            print(f'현재 핸들러 확인 : {wd.current_window_handle}')
            break
    print("웹뷰로 전환 성공")


def change_native_contexts(wd):
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)
    # 네이티브로 전환
    wd.switch_to.context('NATIVE_APP')
    print("네이티브 변환 성공")
