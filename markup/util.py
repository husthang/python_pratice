# encoding: utf-8
# 注意generator的用法、yield用法


def lines(file):
    for line in file:
        yield line
    yield '\n'


def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
