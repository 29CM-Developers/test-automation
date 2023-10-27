# Home 탭으로 이동 딥링크
def move_to_home(self, wd):
    wd.get(self.conf['deeplink']['home'])


def move_to_category(self, wd):
    wd.get(self.conf['deeplink']['category'])


def move_to_like(self, wd):
    wd.get(self.conf['deeplink']['like'])


def move_to_my(self, wd):
    wd.get(self.conf['deeplink']['my'])
