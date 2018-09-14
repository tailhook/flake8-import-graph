import ast
import os.path
from . import __version__


def is_prefix(a, b):
    return a == b[:len(a)]


class ImportVisitor(ast.NodeVisitor):

    def __init__(self, current_module, dest, denied):
        self.dest = dest
        self.current_module = current_module
        mod_path = current_module.split('.')
        self.mod_path = mod_path
        self.denied = [v for k, v in denied if is_prefix(mod_path, k)]

    def visit_Import(self, node):  # noqa: N802
        for name in node.names:
            if self.not_allowed(name.name):
                self.dest.append((
                    node.lineno, node.col_offset,
                    'IMP001 Denied import {}'.format(name.name),
                    'ImportGraphChecker'))

    def visit_ImportFrom(self, node):  # noqa: N802
        if node.level > 0:
            mod_path = self.mod_path[:-node.level]
            if node.module:
                mod_path.append(node.module)
            mod_name = '.'.join(mod_path)
        else:
            mod_name = node.module
        if self.not_allowed(mod_name):
            self.dest.append((
                'IMP001',
                node.lineno, node.col_offset,
                'Denied import {}'.format(name.name)))
        for name in node.names:
            full = mod_name + '.' + name.name
            if self.not_allowed(full):
                self.dest.append((
                    node.lineno, node.col_offset,
                    'IMP001 Denied import {}'.format(name.name),
                    'ImportGraphChecker'))


    def not_allowed(self, name):
        dotted = name.split('.')
        for item in self.denied:
            if is_prefix(item, dotted):
                return True

class ImportGraphChecker:
    name = "import-graph"
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        path = os.path.splitext(filename)[0]
        mod_path = []
        while path:
            if os.path.exists(os.path.join(path, '.flake8')):
                break
            dir, name = os.path.split(path)
            mod_path.append(name)
            path = dir
        self.module = '.'.join(mod_path)

    @classmethod
    def parse_options(cls, options):
        cls.denied_imports = []
        for item in options.deny_imports:
            src, dest = item.split('=', 1)
            cls.denied_imports.append((src.split('.'), dest.split('.')))

    def run(self):
        errors = []
        visitor = ImportVisitor(self.module, errors, self.denied_imports)
        visitor.visit(self.tree)
        yield from errors

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--deny-imports', type='str', comma_separated_list=True,
            default=[], parse_from_config=True,
            help='A list of denied imports like '
                 '`mypkg.where=other_pkg.disallowed_sub_package`.',
        )
