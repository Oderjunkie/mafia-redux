from parsimonious import Grammar, NodeVisitor
from operator import methodcaller

grammar = Grammar(r"""
document = __? (def __?)+
def = classdef / funcdef
classdef = CLASS _ classdesc _? (LBRACKET _? name _? RBRACKET _?)? NEWLINE classbody _? END
funcdef = DEF _ desc _? NEWLINE funcbody _? END
classdesc = name  _? ('-' _? string)?
desc = name _? args _? ('-' _? string)?
name = ~r'[.!?~][a-zA-Z_]+'
string = ~r'[^\r\n]+'
argstring = ~r'[^\r\n \t\$\(\)]+'
args = (_? arg)*
arg = LBRACKET argname RBRACKET
argname = ~'\*?[a-zA-Z]+'
classbody = (__? funcdef NEWLINE)* NEWLINE?
funcbody = (__? stat NEWLINE)* NEWLINE?
stat = fncall / ifstat / forstat / set
fncall = name (_ fnarg)*
fnarg = fullargstring / dollar / variable / number / boolean / argstring
dollar = OPENDOLLAR stat CLOSEDOLLAR
fullargstring = QUOTE ~r'[^\r\n\t\"\+\$\(\)]*' QUOTE
ifstat = IF _ fnarg NEWLINE funcbody _? END
forstat = FOR _ variable _ fnarg NEWLINE funcbody _? END
set = variable _? EQUALS _? fnarg
variable = LBRACKET _? argname _? RBRACKET
number = ~r'([0-9]*\.)?[0-9]+'
boolean = 'true' / 'false'

_ = ~r'[ \t]+'
__ = ~r'[ \t\r\n]+'
IF = 'if'
FOR = 'for'
DEF = 'def'
THEN = 'then'
CLASS = 'class'
LBRACKET = '['
RBRACKET = ']'
OPENDOLLAR = '$('
CLOSEDOLLAR = ')'
EQUALS = '='
QUOTE = '"'
END = 'end'
NEWLINE = ~r'[\r\n]+'
""")

class Code:
    class IfStat:
        def __init__(self, cond, body):
            self.cond = cond
            self.body = body
        def __iter__(self):
            return iter(self.body)
        def __repr__(self):
            return 'IfStat({!r}, {!r})'.format(self.cond, self.body)
        def __str__(self):
            return 'if {}\n{}\nend'.format(self.cond, '\n'.join(map(str, self.body)))
    class ForStat:
        def __init__(self, arr, el, body):
            self.arr = arr
            self.el = el
            self.body = body
        def __iter__(self):
            return iter(self.body)
        def __repr__(self):
            return 'ForStat({!r}, {!r}, {!r})'.format(self.arr, self.el, self.body)
        def __str__(self):
            return 'for {} {}\n{}\nend'.format(self.el, self.arr, self.body)
    class Variable:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return 'Variable({!r})'.format(self.name)
        def __str__(self):
            return '[{}]'.format(self.name)
    class Set:
        def __init__(self, var, val):
            self.var = var
            self.val = val
        def __repr__(self):
            return 'Set({!r}, {!r})'.format(self.var, self.val)
        def __str__(self):
            return '[{}] = {}'.format(self.var, self.val)
    class FuncCall:
        def __init__(self, name, args):
            self.name = name
            self.args = args
        def __repr__(self):
            return 'FuncCall({!r}, {!r})'.format(self.name, self.args)
        def __str__(self):
            return '{} {}'.format(self.name, ' '.join(map(str, self.args)))
    class FuncDef:
        def __init__(self, name, args, docs):
            self.name = name
            self.args = args
            self.docs = docs
            self.body = []
        def __iter__(self):
            return iter(self.body)
        def __repr__(self):
            return 'FuncDef({!r}, {!r}, {!r}, {!r})'.format(self.name, self.args, self.docs, self.body)
        def __str__(self):
            docs = self.docs
            string = 'def {0} {1} - {2}' if docs else 'def {0} {1}'
            args = self.args
            args = map('[{}]'.format, args)
            args = ' '.join(args)
            string = string.format(self.name, args, docs)
            body = map(lambda x:'  '+str(x), self.body)
            funcdef = '{}\n{}\nend'.format(string, '\n'.join(body))
            return funcdef
    class ClassDef:
        def __init__(self, name, docs):
            self.name = name
            self.docs = docs
            self.body = []
            self.inherit = None
        def __iter__(self):
            return iter(self.body)
        def __repr__(self):
            return 'ClassDef({!r}, {!r}, {!r}, {!r})'.format(self.name, self.docs, self.body, self.inherit)
        def __str__(self):
            return '\n'.join(map(str, self.body))
    class Document:
        def __init__(self, defs):
            self.defs = defs
        def __iter__(self):
            return iter(self.defs)
        def __repr__(self):
            return 'Documuent({!r})'.format(self.defs)
        def __str__(self):
            return '\n'.join(map(str, self.defs))

class TrickOrTreater(NodeVisitor):
    def generic_visit(self, node, visited_children):
        return visited_children or node
    def visit__(self, node, visited_children):
        return None
    def visit___(self, node, visited_children):
        return None
    def visit_NEWLINE(self, node, visited_children):
        return None
    def visit_DEF(self, node, visited_children):
        return node.text
    def visit_CLASS(self, node, visited_children):
        return node.text
    def visit_LBRACKET(self, node, visited_children):
        return node.text
    def visit_RBRACKET(self, node, visited_children):
        return node.text
    def visit_END(self, node, visited_children):
        return node.text
    def visit_string(self, node, visited_children):
        return node.text
    def visit_argstring(self, node, visited_children):
        return node.text
    def visit_boolean(self, node, visited_children):
        return node.text=='true'
    def visit_number(self, node, visited_children):
        try:
            return int(node.text)
        except Exception:
            return float(node.text)
    def visit_fullargstring(self, node, visited_children):
        return visited_children[1].text
    def visit_argname(self, node, visited_children):
        return node.text
    def visit_name(self, node, visited_children):
        return node.text
    def visit_fnarg(self, node, visited_children):
        return visited_children[0]
    def visit_def(self, node, visited_children):
        return visited_children[0]
    def visit_variable(self, node, visited_children):
        return Code.Variable(visited_children[2])
    def visit_ifstat(self, node, visited_children):
        return Code.IfStat(visited_children[2], visited_children[4])
    def visit_forstat(self, node, visited_children):
        return Code.ForStat(visited_children[4], visited_children[2], visited_children[6])
    def visit_set(self, node, visited_children):
        return Code.Set(visited_children[0], visited_children[4])
    def visit_desc(self, node, visited_children):
        funcname = visited_children[0]
        args = visited_children[2]
        if type(args)==list:
            args = list(map(methodcaller('__getitem__', 1), args))
            args = list(map(methodcaller('__getitem__', 1), args))
        else:
            args = []
        desc = visited_children[4]
        if type(desc)==list:
            desc = desc[0][2]
        else:
            desc = ''
        return Code.FuncDef(funcname, args, desc)
    def visit_classdesc(self, node, visited_children):
        funcname = visited_children[0]
        desc = visited_children[2]
        if type(desc)==list:
            desc = desc[0][2]
        else:
            desc = ''
        return Code.ClassDef(funcname, desc)
    def visit_funcdef(self, node, visited_children):
        assert visited_children[0]=='def'
        assert visited_children[1]==None
        visited_children[2].body = visited_children[5]
        return visited_children[2]
    def visit_classdef(self, node, visited_children):
        assert visited_children[0]=='class'
        assert visited_children[1]==None
        if type(visited_children[4])==list:
            visited_children[2].inherit = visited_children[4][0][2]
        visited_children[2].body = visited_children[6]
        return visited_children[2]
    def visit_funcbody(self, node, visited_children):
        return list(map(methodcaller('__getitem__', 1), visited_children[0]))
    def visit_classbody(self, node, visited_children):
        return list(map(methodcaller('__getitem__', 1), visited_children[0]))
    def visit_stat(self, node, visited_children):
        return visited_children[0]
    def visit_fncall(self, node, visited_children):
        funcname = visited_children[0]
        args = []
        if type(visited_children[1])==list:
            args = list(map(methodcaller('__getitem__', 1), visited_children[1]))
        return Code.FuncCall(funcname, args)
    def visit_dollar(self, node, visited_children):
        return visited_children[1]
    def visit_document(self, node, visited_children):
        return Code.Document(list(map(methodcaller('__getitem__', 0), visited_children[1])))

def parse(code):
    return TrickOrTreater().visit(grammar.parse(code))

from types import CodeType, FunctionType

class new:
    class classes:
        pass
    class funcs:
        pass
    def __init__(self):
        pass
    def main(self, code):
        ast = parse(code)
        for defi in ast.defs:
            if type(defi)==Code.FuncDef:
                setattr(self.funcs, *self.register_func(defi))
            elif type(defi)==Code.ClassDef:
                setattr(self.classes, *self.register_class(defi))
    def register_class(self, defi):
        def init(self):
            pass
        funcobjs = []
        assert defi.name[0]=='.'
        classname = defi.name[1:]
        for func in defi:
            assert func.name[0]=='.'
            funcobjs.append(self.register_func(func))
        options = {'__init__': init}
        for funcname, funcobj in funcobjs:
            options.update({funcname: funcobj})
        return classname, type(classname, (object,), options)
    def register_func(self, defi):
        funcname = defi.name[1:]
        consts = (None, *self.find_consts(defi))
        names = self.find_names(defi)
        local = self.find_locals(defi)
        args = ('io', *defi.args)
        code = self.code_gen(defi, consts, names, (*args, *local)) + b'd' + bytes([consts.index(None)]) + b'S\x00'
        funcobj = self.converttofunc(defi, funcname, consts, names, code, args, local)
        return funcname, funcobj
    def converttofunc(self, func, name, consts, names, code, args, local):
        co_varnames = args+local
        co_consts = consts
        co_flags = 67
        co_argcount = len(args)
        if len(co_varnames)>0 and co_varnames[-1][0]=='*':
            co_flags = 71
            co_varnames[-1] = co_varnames[-1][1:]
            co_argcount -= 1
        co_filename = self.__init__.__code__.co_filename
        co_name = name
        co_firstlineno = 1
        co_freevars = ()
        co_kwonlyargcount = 0
        co_lnotab = b'\x00\x01'
        co_names = names
        co_nlocals = co_argcount+len(local)
        co_posonlyargcount = 0
        co_kwonlyargcount = 0
        co_stacksize = 1
        co_cellvars = ()
        co_code = code
        codeobj = CodeType(co_argcount, co_posonlyargcount, co_kwonlyargcount, co_nlocals, co_stacksize,
                           co_flags, co_code, co_consts, co_names, tuple(co_varnames), co_filename, co_name,
                           co_firstlineno, co_lnotab, co_freevars, co_cellvars)
        func = FunctionType(codeobj, globals(), name=co_name)
        return func
    def find_consts(self, func):
        if type(func) in [str, int, float, bool]:
            return [func]
        consts = []
        for stat in func:
            if type(stat) in [str, int, float, bool]:
                consts.append(stat)
                continue
            if type(stat)==Code.FuncCall:
                for arg in stat.args:
                    if type(arg) in [str, int, float, bool] and arg not in consts:
                        consts.append(arg)
                        continue
                    if type(arg)==Code.FuncCall:
                        for el in self.find_consts([arg]):
                            if el not in consts:
                                consts.append(el)
                continue
            if type(stat)==Code.IfStat:
                for el in [*self.find_consts(stat), *self.find_consts([stat.cond])]:
                    if el not in consts:
                        consts.append(el)
                continue
            if type(stat)==Code.ForStat:
                for el in [*self.find_consts(stat), *self.find_consts([stat.arr])]:
                    if el not in consts:
                        consts.append(el)
                continue
            elif type(stat)==Code.Set:
                for el in self.find_consts([stat.val]):
                    if el not in consts:
                        consts.append(el)
        return tuple(consts)
    def convert_to_name(self, name):
        if name[0] in '!?':
            return '_on_'+name[1:]
        elif name[0] in '.~':
            return name[1:]
    def find_names(self, func):
        names = []
        for stat in func:
            if type(stat)==Code.FuncCall:
                name = self.convert_to_name(stat.name)
                if name not in names:
                    names.append(name)
                for arg in stat.args:
                    if type(arg)==Code.FuncCall:
                        for el in self.find_names([arg]):
                            if el not in names:
                                names.append(el)
            elif type(stat)==Code.IfStat:
                for el in [*self.find_names(stat), *self.find_names([stat.cond])]:
                    if el not in names:
                        names.append(el)
            elif type(stat)==Code.ForStat:
                for el in [*self.find_names(stat), *self.find_names([stat.arr])]:
                    if el not in names:
                        names.append(el)
            elif type(stat)==Code.Set:
                if type(stat.val)==Code.FuncCall:
                    for el in self.find_names([stat.val]):
                        if el not in names:
                            names.append(el)
        return tuple(names)
    def find_locals(self, func):
        local = []
        for stat in func:
            if type(stat)==Code.IfStat:
                for el in self.find_locals(stat):
                    if el not in local:
                        local.append(el)
            elif type(stat)==Code.ForStat:
                for el in [*self.find_locals(stat), stat.el.name]:
                    if el not in local:
                        local.append(el)
            elif type(stat)==Code.Set:
                if stat.var not in local:
                    local.append(stat.var.name)
        return tuple(local)
    def code_gen(self, func, consts, names, args):
        final = b''
        for stat in func:
            if type(stat)==Code.FuncCall:
                final += self.code_gen_call(stat, consts, names, args)
                continue
            if type(stat)==Code.IfStat:
                final += self.code_gen_if(len(final), stat, consts, names, args)
                continue
            if type(stat)==Code.ForStat:
                final += self.code_gen_for(len(final), stat, consts, names, args)
                continue
            if type(stat)==Code.Set:
                final += self.code_gen_set(stat, consts, names, args)
                continue
        return final
    def code_gen_if(self, ln, func, consts, names, args):
        body = self.code_gen(func.body, consts, names, args)
        cond = self.code_gen_call(func.cond, consts, names, args)
        bln = len(body)
        cln = len(cond)
        pointer = ln+cln+2+bln
        if pointer < 256:
            return cond + b'r' + bytes([pointer]) + body
        pointerlo = pointer%0x100
        pointerhi = pointer//0x100
        return cond + b'\x90' + bytes([pointerhi]) + b'r' + bytes([pointerlo]) + body
    def code_gen_for(self, ln, func, consts, names, args):
        body = self.code_gen(func.body, consts, names, args)
        arr = self.code_gen_call(func.arr, consts, names, args)
        el = args.index(func.el.name)
        bln = len(body)
        aln = len(arr)
        plus = bln+6
        minus = ln+aln+2
        plusjump = b']' + bytes([plus%0x100])
        if plus>255:
            plusjump = b'\x90' + bytes(plus//0x100) + plusjump
        minusjump = b'q' + bytes([minus%0x100])
        if minus>255:
            minusjump = b'\x90' + bytes(minus//0x100) + minusjump
        code = arr + b'D\x00' + plusjump +\
               b'}' + bytes([el]) + body + b'\x01\x00' + \
               minusjump
        return code
    def code_gen_call(self, stat, consts, names, args):
        if type(stat) in [str, bool, int, float]:
            return b'd' + bytes([consts.index(stat)])
        if type(stat)==Code.Variable:
            return b'|' + bytes([args.index(stat.name)])
        final = b''
        name = self.convert_to_name(stat.name)
        name = names.index(name)
        final += b'|' + (bytes([args.index('io')]) if stat.name[0]=='~' else b'\x00') + b'\xa0' + bytes([name])
        for arg in stat.args:
            if type(arg) in [str, bool, int, float]:
                final += b'd' + bytes([consts.index(arg)])
            if type(arg)==Code.FuncCall:
                final += self.code_gen_call(arg, consts, names, args)
            if type(arg)==Code.Variable:
                final += b'|' + bytes([args.index(arg.name)])
        final += b'\xa1' + bytes([len(stat.args)])
        return final
    def code_gen_set(self, stat, consts, names, args):
        name = args.index(stat.var.name)
        val = stat.val
        final = b'}' + bytes([name])
        if type(val) in [str, bool, int, float]:
            return b'd' + bytes([consts.index(val)]) + final
        if type(val)==Code.FuncCall:
            return self.code_gen_call(val, consts, names, args) + final
        if type(val)==Code.Variable:
            return b'|' + bytes([args.index(val.name)]) + final