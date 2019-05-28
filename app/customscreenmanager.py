# -*- coding: utf-8 -*-

__all__ = ('MostxScreenManager', )


from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager


class MostxScreenManager(ScreenManager):
    def try_to_switch_screen(self, name, transition=None):
        '''Screenを切り替えるmethod
        戻り値:
            True  切り替え成功
            False 切り替え失敗
        以前の切り替えが終わってない時に別のtransitionを使って次の切り替えを行おうとすると表示がおかしくなるので、
        そうならないように確認している。また切り替えようとしたScreenが存在しない時には、例外を投げるのではなくlog
        にその事を書き残すだけである。これはその方が各Screenを単体testする時に都合が良いからです。
        '''
        if self.transition.is_active:
            Logger.warning(f"MostxApp: You can't switch screen until the previous transition is done.")
            return False
        if not self.has_screen(name):
            Logger.warning(f"MostxApp: No screen named '{name}'")
            return False
        if transition is not None:
            self.transition = transition
        self.current = name
        return True
