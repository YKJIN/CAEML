__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from pyparsing import Optional, pyparsing_common, Or, Forward, QuotedString, ZeroOrMore, OneOrMore


class File(object):
    def __init__(self, aStr, location, tokens):
        self.paragraphs = tokens.asDict()['paragraphs']

    def __repr__(self):
        return '\n'.join(str(p) for p in self.paragraphs)

    def ca_repr(self):
        return '\n'.join((p.ca_repr()) for p in self.paragraphs)


class Paragraph(object):
    def __init__(self, aStr, location, tokens):
        td = tokens.asDict()
        self.left_side = tokens.asDict()['left_side'] if 'left_side' in tokens.asDict() else None
        self.keyword_arguments = tokens.asDict()[
            'keyword_arguments'] if 'keyword_arguments' in tokens.asDict() else None
        self.operator_name = tokens.asDict()['operator_name'] if 'operator_name' in tokens.asDict() else None

    def __repr__(self):
        return '{0}={1}\n\t{2}\n'.format(self.left_side, self.operator_name, self.keyword_arguments)

    def ca_repr(self):
        left_text = self.left_side
        operator_text = self.operator_name
        kwa_text = self.keyword_arguments.ca_repr() if self.keyword_arguments else '()'
        if left_text:
            return '{0}={1}({2});'.format(left_text, operator_text, kwa_text)
        if kwa_text == '()':
            return '{1}{2};'.format(left_text, operator_text, kwa_text)
        return '{1}({2});'.format(left_text, operator_text, kwa_text)


class Expression(object):
    def __init__(self, aStr, location, tokens):
        td = tokens.asDict()
        assert (len(td) == 1)
        tl = list(tokens.asDict().values())
        self.expression = tl[0]

    def __repr__(self):
        return '{0}'.format(str(self.expression))

    def ca_repr(self):
        if (isinstance(self.expression, Keyword_arguments)):
            return '_F({0})'.format(self.expression.ca_repr())

        if (isinstance(self.expression, Value)):
            return '{0}'.format(self.expression.ca_repr())

        return '({0})'.format(self.expression.ca_repr())


class Keyword_arguments(object):
    def __init__(self, aStr, location, tokens):
        td = tokens.asDict()
        self.keyword_arguments = tokens.asDict()['keyword_argument']

    def findValueForKeyRecursive(self, key):
        myKeys = [kvp.keyword for kvp in self.keyword_arguments]
        if key in myKeys:
            for kvp in self.keyword_arguments:
                if kvp.keyword == key:
                    return kvp.argument
            raise Exception('unreachbale')

        for kvp in self.keyword_arguments:
            if (isinstance(kvp.argument, Keyword_arguments)):
                recursive_argument = kvp.argument.findValueForKeyRecursive(key)
                if recursive_argument:
                    return recursive_argument

            if (isinstance(kvp.argument, Expression)):
                if (isinstance(kvp.argument.expression, Keyword_arguments)):
                    recursive_argument = kvp.argument.expression.findValueForKeyRecursive(key)
                    if recursive_argument:
                        return recursive_argument

        return None

    def __repr__(self):
        if (len(self.keyword_arguments) == 1):
            return str(self.keyword_arguments)
        return ', '.join(str(v) for v in self.keyword_arguments)

    def ca_repr(self):
        if (len(self.keyword_arguments) == 1):
            return (self.keyword_arguments[0].ca_repr()) + ','
        return ',\n\t\t\t'.join(v.ca_repr() for v in self.keyword_arguments) + ','


class Keyword_argument(object):
    def __init__(self, aStr, location, tokens):
        td = tokens.asDict()
        self.keyword = tokens.asDict()['keyword']
        self.argument = tokens.asDict()['expression']

    def __repr__(self):
        return '{{{0}:{1}}}'.format(str(self.keyword), str(self.argument))

    def ca_repr(self):
        return '{0}={1}'.format(str(self.keyword), str(self.argument.ca_repr()))


class Values(object):
    def __init__(self, aStr, location, tokens):
        td = tokens.asDict()
        self.values = tokens.asDict()['valueList']

    def __repr__(self):
        return str(self.values)

    def ca_repr(self):
        return ','.join(v.ca_repr() for v in self.values) + ','


class Value(object):
    def __init__(self, aStr, location, tokens):
        td = tokens.asDict()
        if 'id' in td:
            self.value = td['id']
        elif 'number' in td:
            self.value = td['number']
        else:
            self.value = "'" + td['string'] + "'"

    def __repr__(self):
        return str(self.value)

    def ca_repr(self):
        return str(self)


class CodeAster_commFile_Model(object):
    def __init__(self, comm_file_path):
        expression_spaced = Forward()
        expression = Forward()
        args_spaced = Forward()

        cb = Optional(',') + ')'  # closing_brackets might include a ','
        ob = Optional(' ') + '(' + Optional(' ')  # closing_brackets might include a ' '

        value = (Or([pyparsing_common.identifier.copy().setResultsName('id'),
                     pyparsing_common.number.copy().setResultsName('number'),
                     QuotedString("'").setResultsName('string')])).setParseAction(Value).setResultsName('value')

        values = (ZeroOrMore(value.setResultsName('valueList', listAllMatches=True) + Optional(','))).setParseAction(
            Values)

        keyword = pyparsing_common.identifier.copy()

        keyword_argument = (
            keyword.setResultsName('keyword') + '=' + expression_spaced.setResultsName('expression')
        ).setParseAction(Keyword_argument)

        keyword_arguments = (
            keyword_argument.setResultsName('keyword_argument', listAllMatches=True) +
            ZeroOrMore(',' + keyword_argument.setResultsName('keyword_argument', listAllMatches=True))
        ).setParseAction(Keyword_arguments)

        expression << (Or([
            value, (ob + values.setResultsName('values') + cb),
            '_F' + ob + keyword_arguments.setResultsName('keyword_arguments') + cb,
            ob + expression.setResultsName('expression') + cb
        ])).setParseAction(Expression)

        expression_spaced << (Or([expression, ob + expression_spaced + cb]))

        left_side = pyparsing_common.identifier.setResultsName('left_side')
        operator_name = pyparsing_common.identifier.setResultsName('operator_name')
        paragraph = (Optional(left_side + "=") + operator_name + ob + Optional(keyword_arguments
            .setResultsName(
            'keyword_arguments')) + cb + Optional(';')).setParseAction(Paragraph)

        file = OneOrMore(paragraph).setResultsName('paragraphs').setParseAction(File)

        self.beam_data_model = file.parseFile(comm_file_path)
