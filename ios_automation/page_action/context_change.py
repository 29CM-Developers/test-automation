def switch_context(wd, context):
    if context == 'native':
        wd.switch_to.context(wd.contexts[0])
    elif context == 'webview' and len(wd.contexts) > 1:
        wd.switch_to.context(wd.contexts[-1])
