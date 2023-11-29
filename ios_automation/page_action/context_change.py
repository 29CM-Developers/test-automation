def switch_context(wd, context):
    native = wd.contexts[0]
    webview = wd.contexts[-1]
    if context == 'native':
        wd.switch_to.context(native)
    elif context == 'webview':
        wd.switch_to.context(webview)
    print(f'{wd.current_context} 전환 완료')
