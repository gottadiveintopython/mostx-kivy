# -*- coding: utf-8 -*-
'''
Button付きのPopupを簡単に作れる


例えば[Yes][No]Buttonの付いたPopupを使って利用者に質問したい時は

yesno_popup = PopupWithButtons(
    content=Label(text='Do you like Kivy?'),
    button_texts=('Yes', 'No', ),
)
yesno_popup.bind(on_button_press=(
    lambda popup, button: print(button.text, 'was pressed.')
))
yesno_popup.open()

とすればいい。もし`auto_dismiss`をFalseにした場合は、Buttonを押しても自動でPopupが
閉じなくなるので、以下のようにCallback関数内で明示的に閉じる必要がある。

yesno_popup = PopupWithButtons(
    content=Label(text='Do you like Kivy?'),
    button_texts=('Yes', 'No', ),
    auto_dismiss=False,  # 相違点
)
yesno_popup.bind(on_button_press=(
    lambda popup, button: popup.dismiss()  # 相違点
))
yesno_popup.open()
'''

__all__ = ('PopupWithButtons', )

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import (
    ObjectProperty, ListProperty,
)


Builder.load_string(r"""
<PopupWithButtons>:
    _container: container
    _buttons_layout: buttons_layout
    BoxLayout:
        size: root.size
        orientation: 'vertical'
        padding: '5sp'
        spacing: '5sp'
        RelativeLayout:
            id: container
        BoxLayout:
            id: buttons_layout
            size_hint_y: 0.1
            padding: '5sp'
            spacing: '5sp'
""")


class PopupWithButtons(Factory.ModalView):

    button_class = ObjectProperty(Factory.Button)
    '''使用するButtonを任意の物に置き換えられる'''

    content = ObjectProperty(baseclass=Factory.Widget)
    '''PopupのMainとなる中身。このWidgetの下にButtonが並べられる'''

    button_texts = ListProperty(['OK', ])
    '''Buttonに表示する文字列のlist。このlistの要素数だけButtonが作られる。'''

    _container = ObjectProperty(baseclass=Factory.Widget)
    _buttons_layout = ObjectProperty(baseclass=Factory.Widget)

    __events__ = ('on_button_press', 'on_button_release', )

    def on_button_press(self, *args):
        if self.auto_dismiss:
            self.dismiss()

    def on_button_release(self, *args):
        if self.auto_dismiss:
            self.dismiss()

    def _on_button_press(self, button):
        self.dispatch('on_button_press', button)

    def _on_button_release(self, button):
        self.dispatch('on_button_release', button)

    def on_content(self, __, widget):
        if self._container is not None:
            self._refresh_container()

    def on__container(self, __, container):
        if container is not None and self.content is not None:
            self._refresh_container()

    def _refresh_container(self):
        container = self._container
        container.clear_widgets()
        container.add_widget(self.content)

    def on_button_texts(self, __, button_texts):
        if self._buttons_layout is not None:
            self._refresh_buttons_layout()

    def on__buttons_layout(self, __, layout):
        if layout is not None:
            self._refresh_buttons_layout()

    def _refresh_buttons_layout(self):
        layout = self._buttons_layout
        layout.clear_widgets()
        layout_add_widget = layout.add_widget
        button_class = self.button_class
        for text in self.button_texts:
            button = button_class(text=str(text))
            button.bind(
                on_press=self._on_button_press,
                on_release=self._on_button_release,
            )
            layout_add_widget(button)


def _test():
    from kivy.base import runTouchApp

    yesno_popup = PopupWithButtons(
        content=Factory.Label(text='Do you like Kivy?'),
        button_texts='Yes No'.split(),
    )
    yesno_popup.bind(on_button_press=(
        lambda popup, button: print(button.text, 'was pressed.')
    ))

    ok_popup = PopupWithButtons(
        content=Factory.Label(text='"The armor I used to seal my all too '
                                   'powerful strength is now broken."'),
        button_texts=('OK', ),
    )

    pick_color_popup = PopupWithButtons(
        content=Factory.ColorPicker(),
        button_texts='OK Cancel'.split(),
        auto_dismiss=False,
    )
    def on_button_press(popup, button):
        if button.text == 'Cancel':
            print('Cancelled.')
        elif button.text == 'OK':
            print('Color', popup.content.color, 'was choosed.')
        popup.dismiss()
    pick_color_popup.bind(on_button_press=on_button_press)

    root = Builder.load_string(r"""
BoxLayout:
    orientation: 'vertical'
    spacing: '5sp'
    padding: '5sp'
    Button:
        id: yesno
        text: 'Yes No Popup'
    Button:
        id: ok
        text: 'OK Popup'
    Button:
        id: color
        text: 'Pick Color'
""")
    root.ids.yesno.bind(on_press=yesno_popup.open)
    root.ids.ok.bind(on_press=ok_popup.open)
    root.ids.color.bind(on_press=pick_color_popup.open)
    runTouchApp(root)


if __name__ == '__main__':
    _test()
