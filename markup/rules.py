# coding=utf-8
"""
检测块的类型，并调用相应的处理器进行处理；
@file: rules.py
@time: 2018/5/3 20:00
@author: liuhang
@email: liuhang93@foxmail.com
"""


class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


class HeadingRule(Rule):
    """
    标题，标题占一行，最多70个字符，不以冒号结尾
    """
    type = 'heading'

    def condition(self, block):
        return len(block) <= 70 and not block[-1] == ':' and not '\n' in block


class TitleRule(HeadingRule):
    """
    题目，第一个标题，继承自HeadingRule
    """
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        # 调用超类用法
        return HeadingRule.condition(self, block)


class ListItemRule(Rule):
    """
    列表项
    """
    type = 'list_item'

    # @staticmethod
    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        # return super().action(block, handler)
        return True


class ListRule(ListItemRule):
    type = 'list'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False


class ParagraphRule(Rule):
    type = 'paragraph'

    def condition(self, block):
        return True
