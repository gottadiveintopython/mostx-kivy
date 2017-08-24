# -*- coding: utf-8 -*-

r'''意図しない属性の書き換えを防ぐ機能 と 冗長な記述を防ぐ機能を持つオブジェクト
(python2/python3両対応)

更新日(2017/04/24)

現状、Pythonのオブジェクトにはいかの問題があると思う。

1. 既存の属性に書き込んだつもりが、新しく別の属性を作ってしまう。
obj.time = 100
obj.tine = 90  # miss typing

2. 何度も同じオブジェクトの属性に値を入れる時、記述が冗長。
obj.attr1 = 1
obj.attr2 = 2  # annoying
obj.attr3 = 3  # annoying

このモジュールのSmartObjectでは以下の様に問題が解消されている
obj = SmartObject(attr1=1, attr2=1)  # 作る時は自由に属性を決めれる
obj.attr1 = 1                        # OK
obj.attr3 = 1                        # AttributeError! "attr3" doesn't exist
obj.so_overwrite(attr1=2, attr2=2)   # OK
obj.so_overwrite(attr1=3, attr3=3)   # AttributeError! "attr3" doesn't exist
obj.so_update(attr1=4, attr3=4)      # OK "so_update" is able to create new attributes.

又、以下の様にobjを読み取り専用にする事も可能
ro = obj.so_as_readonly()  #  make it read only
print(ro.attr1)            #  OK
ro.attr1 = 0               #  AttributeError! It's read only
ro.so_overwrite(attr1=0)   #  AttributeError! It's read only
ro.so_update(attr1=0)      #  AttributeError! It's read only
temp = ro.so_as_writable() #  make it back writable
temp.attr1 = 0             #  OK

so_nameはSmartObjectに付けれる任意の名前で、Error時やprintに使われる。
'''

__all__ = (r'SmartObject', )


class ReadOnly(object):
    r'internal use'

    def __init__(self, obj):
        self.__dict__[r'__obj'] = obj

    def so_raise_error(self):
        r'internal use'
        raise AttributeError(
            r"You can't set attributes through 'ReadOnly' object"
        )

    def __getattr__(self, key):
        return getattr(self.__dict__[r'__obj'], key)

    def __setattr__(self, key, value):
        self.so_raise_error()

    def __str__(self):
        return self.__dict__[r'__obj'].__str__()

    def so_overwrite(self, **kwargs):
        self.so_raise_error()

    def so_update(self, **kwargs):
        self.so_raise_error()

    def so_as_readonly(self):
        return self

    def so_as_writable(self):
        return self.__dict__[r'__obj']

    def so_to_dict(self):
        return self.__dict__[r'__obj'].to_dict()

    def so_copy(self):
        return self.__dict__[r'__obj'].so_copy()


class SmartObject(object):

    def __init__(self, **kwargs):
        self.__dict__[r'so_name'] = r'SmartObject'
        self.so_update(**kwargs)

    def __getattr__(self, key):
        raise AttributeError(
            r"'{}' has no attribute named '{}'.".format(
                self.__dict__[r'so_name'],
                key))

    def __setattr__(self, key, value):
        r'''overwrite a attribute that already exist'''
        if self.__dict__.__contains__(key):
            self.__dict__[key] = value
        else:
            raise AttributeError(
                r"'{}' has no attribute named '{}'.".format(
                    self.__dict__[r'so_name'],
                    key)
            )

    def __str__(self):
        temp = [self.so_name]
        temp.extend(
            '{} : {}'.format(key, value) for key, value in self.__dict__.items()
            if not key.startswith(r'so_')
        )
        return '\n  '.join(temp)

    def so_overwrite(self, **kwargs):
        r'''overwrite attributes that already exist'''
        for (key, value) in kwargs.items():
            if self.__dict__.__contains__(key):
                self.__dict__[key] = value
            else:
                raise AttributeError(
                    r"'{}' has no attribute named '{}'.".format(
                        self.__dict__[r'so_name'],
                        key)
                )

    def so_update(self, **kwargs):
        self.__dict__.update(kwargs)

    def so_as_readonly(self):
        return ReadOnly(self)

    def so_as_writable(self):
        return self

    def so_to_dict(self):
        return self.__dict__.copy()

    def so_copy(self):
        return SmartObject(**self.__dict__)


def _test():
    obj = SmartObject(
        so_name='Sukina Tabemono',
        kudamono=r'ringo',
        yasai=r'naganegi',
        okashi=r'kaki no tane')
    print(obj.so_as_readonly())
    obj.so_update(nomimono=r'mugicha')
    try:
        obj.niku = r'butaniku'
    except AttributeError as e:
        print(e)
    obj2 = obj.so_as_readonly().so_copy()
    obj2.kudamono = r'kaki'
    print(obj)
    print(obj2)


if __name__ == '__main__':
    _test()
