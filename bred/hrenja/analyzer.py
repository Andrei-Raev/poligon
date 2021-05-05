def pprint(obj):
    print(obj.__class__.__name__)
    print(f'\tstr: {obj}')
    print(f'\ttype: {type(obj)}')
    print(f'\t{obj}')


class AnalyzeMessage:
    def __init__(self, message):
        pprint(message.author)
