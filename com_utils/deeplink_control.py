from time import sleep


# Home 탭으로 이동 딥링크
def move_to_home(self, wd):
    wd.get(self.conf['deeplink']['home'])


def move_to_category(self, wd):
    wd.get(self.conf['deeplink']['category'])


def move_to_like(self, wd):
    wd.get(self.conf['deeplink']['like'])


def move_to_my(self, wd):
    wd.get(self.conf['deeplink']['my'])


def move_to_welove(self, wd):
    wd.get(self.conf['deeplink']['welove'])


def move_to_pdp(wd, product_item_no):
    wd.get(f'app29cm://product/{product_item_no}')
    sleep(3)
