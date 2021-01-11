

class CodeBlockNested():
    def __init__(self, code_type, head, block, foot=None):
        self.code_type = code_type
        self.head = head
        self.block = block
        self.foot = foot
    def __str__(self, indent=''):
        if self.code_type == 'html':
            result = indent + self.head + '\n'
        else:
            result = indent + self.head + ':\n'
        indent += '    '
        for block in self.block:
            if isinstance(block, CodeBlockNested):
                result += block.__str__(indent)
            else:
                result += indent + block + '\n'
        if self.code_type == 'html':
            result += self.foot + '\n'
        return result


class CodeBlock():
    def __init__(self, block):
        self.block = block
    def __str__(self):
        result = ''
        for block in self.block:
            if isinstance(block, CodeBlockNested):
                result += block.__str__()
            else:
                result += block + '\n'
        return result