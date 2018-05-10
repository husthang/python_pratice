# coding=utf-8
"""
处理程序,增加相应格式化的标记
@file: handlers.py
@time: 2018/5/3 20:01
@author: liuhang
@email: liuhang93@foxmail.com
"""


class Handler:
    # 函数参数，可变参数的用法
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                result = match.group(0)  # 模式的第0组，
            return result

        return substitution


class HTMLRenderer(Handler):
    def start_document(self):
        print('<html><head><title>')

    def end_document(self):
        print('</body></html>')

    def start_paragrahp(self):
        print('<p>')

    def end_paragrahp(self):
        print('</p>')

    def start_heading(self):
        print('<h2>')

    def end_heading(self):
        print('</h2>')

    def start_list(self):
        print('<ul>')

    def end_list(self):
        print('</ul>')

    def start_list_item(self):
        print('<li>')

    def end_list_item(self):
        print('</li>')

    def start_title(self):
        print('<h1>')

    def end_title(self):
        print('</h1>')

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)  # 模式的第一组

    def sub_url(self, match):
        return '<a href = "%s">%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href = "mailto:%s">%s</a>' % (match.group(1), match.group(1))

    def feed(self, data):
        print(data)
