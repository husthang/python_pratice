# coding=utf-8
"""
主程序
@file: markup.py
@time: 2018/5/3 20:01
@author: liuhang
@email: liuhang93@foxmail.com
"""
import re, sys
from util import *
from rules import *
from handlers import *


class Parser:
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            # 先过滤一遍，识别出email,星号加重，url等
            for each_filter in self.filters:
                block = each_filter(block, self.handler)

            # 对每一段实现html标记，判断该段应该用哪种规则标记
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    def __init__(self, handler):
        super().__init__(handler)
        # Parser.__init__(self, handler)

        # 增加标记规则
        self.add_rule(HeadingRule())
        self.add_rule(TitleRule())
        self.add_rule(ListRule())
        self.add_rule(ListItemRule())
        self.add_rule(ParagraphRule())

        # 增加过滤规则:星号加强，url和email识别
        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(http://[\.a-zA-Z]+)', 'url')
        self.add_filter(r'[\.a-zA-Z]+@[\.a-zA-A]+', 'mail')


handler = HTMLRenderer()
parser = BasicTextParser(handler)
# with open('test.txt') as file:
#     parser.parse(file)
parser.parse(sys.stdin)
