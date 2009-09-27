#!/usr/bin/env python

# Copyright (C) 2009 Osmo Salomaa
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Walk module sources and autogenerate RST documentation files.

Usage: python autogen.py MODULE_NAME...

Requires RST template files 'class.rst.in', 'index.rst.in', 'module.rst.in' and
'source.rst.in' somewhere in templates_path as defined in conf.py. Suggested to
be used with the 'autoclean' extension. Together, this script, the templates
and the 'autoclean' extension should provide decent and complete API
documentation automatically generated from source code with verbose docstrings
written in reStructuredText markup. Additional hand-written documentation can
be added by editing the 'index.rst.in' template to include introductory text or
links to the separate, handwritten files.
"""

import codecs
import imp
import inspect
import jinja2
import os
import sys

conf = os.path.join(os.path.dirname(__file__), "conf.py")
conf = imp.load_source("conf", conf)


def document_class(names, cls):
    """Write RST-file documenting class and its members."""
    print ".".join(names)
    write_template("class",
                   names,
                   anchestors=get_anchestors(cls),
                   cls=".".join(names),
                   cls_short=names[-1],
                   is_exception=issubclass(cls, Exception),
                   methods=get_methods(cls),
                   module=".".join(names[:-1]),
                   source_doc=get_source_doc(cls),
                   source_fname=get_source_fname(cls))

def document_module(names, module):
    """Write RST-file documenting module and its members."""
    print ".".join(names)
    document_source(names, module)
    write_template("module",
                   names,
                   classes=get_classes(module),
                   functions=get_functions(module),
                   module=".".join(names),
                   modules=get_modules(module),
                   root=conf.autogen_output_path,
                   source_doc=get_source_doc(module),
                   source_fname=get_source_fname(module))

    for name in get_modules(module):
        document_module(tuple(names) + (name,),
                        getattr(module, name))

    for name in get_classes(module):
        document_class(tuple(names) + (name,),
                       getattr(module, name))

def document_source(names, module):
    """Write RST-file with module source code."""
    names_out = list(names)
    names_out[-1] = "%s_source" % names_out[-1]
    write_template("source",
                   names_out,
                   module=".".join(names),
                   source_fname=get_source_fname(module),
                   source_include=get_source_include(module))

def filter_members(members):
    """Return subset of members to appear in documentation."""
    if not conf.private_members:
        members = [x for x in members
                   if (not x.startswith("_") or
                       x in conf.include_members)]
    members = set(members) - set(conf.exclude_members)
    return sorted(list(members))

def get_anchestors(cls):
    """Return a list of names of anchestor classes."""
    if not cls.__bases__:
        return []
    base = cls.__bases__[0]
    name = "%s.%s" % (base.__module__, base.__name__)
    name = name.replace("__builtin__.", "")
    return [name] + get_anchestors(base)

def get_classes(module):
    """Return list of names of classes defined in module."""
    is_class = lambda x: inspect.isclass(getattr(module, x))
    classes = filter(is_class, module.__dict__.keys())
    top = module.__name__.split(".")[0]
    for i in reversed(range(len(classes))):
        candidate = getattr(module, classes[i])
        parent = inspect.getmodule(candidate)
        if (parent is None or
            not parent.__name__.startswith(top)):
            classes.pop(i)
    return filter_members(classes)

def get_functions(module):
    """Return list of names of functions defined in module."""
    is_function = lambda x: inspect.isfunction(getattr(module, x))
    functions = filter(is_function, module.__dict__.keys())
    top = module.__name__.split(".")[0]
    for i in reversed(range(len(functions))):
        candidate = getattr(module, functions[i])
        parent = inspect.getmodule(candidate)
        if (parent is None or
            not parent.__name__.startswith(top)):
            functions.pop(i)
    return filter_members(functions)

def get_methods(cls):
    """Return list of names of methods defined in cls."""
    is_method = lambda x: inspect.ismethod(getattr(cls, x))
    methods = filter(is_method, cls.__dict__.keys())
    return filter_members(methods)

def get_modules(module):
    """Return list of names of modules defined in module."""
    is_module = lambda x: inspect.ismodule(getattr(module, x))
    modules = filter(is_module, module.__dict__.keys())
    top = module.__name__.split(".")[0]
    for i in reversed(range(len(modules))):
        candidate = getattr(module, modules[i])
        parent = inspect.getmodule(candidate)
        if (parent is None or
            module.__name__.startswith(parent.__name__) or
            not parent.__name__.startswith(top)):
            modules.pop(i)
    return filter_members(modules)

def get_source_doc(obj):
    """Return path to obj source RST document or None."""
    if get_source_path(obj) is None:
        return None
    dotted_name = None
    if inspect.ismodule(obj):
        dotted_name = obj.__name__
    if inspect.isclass(obj):
        dotted_name = obj.__module__
    if dotted_name is None:
        return None
    return "/%s/%s_source" % (conf.autogen_output_path, dotted_name)

def get_source_fname(obj):
    """Return obj filename relative to project root or None."""
    path = get_source_path(obj)
    if path is None:
        return None
    directory = os.path.dirname(__file__)
    root = os.path.join(directory, conf.project_root)
    root = os.path.abspath(root)
    fname = path.replace(root, "")
    while fname.startswith(os.sep):
        fname = fname[1:]
    return fname

def get_source_include(obj):
    """Return obj filename relative to documentation root or None."""
    fname = get_source_fname(obj)
    if fname is None:
        return None
    return "/%s" % os.path.join(conf.project_root, fname)

def get_source_path(obj):
    """Return absolute path to file obj is defined in or None."""
    try:
        path = inspect.getfile(obj)
    except TypeError:
        return None
    if path.endswith(("pyc", "pyo")):
        path = path[:-1]
    return os.path.abspath(path)

def main(modules):
    """Recursively document all modules."""
    write_template("index",
                   ("index",),
                   project=conf.project,
                   project_url=conf.project_url,
                   modules=modules,
                   root=conf.autogen_output_path)

    for module in modules:
        document_module(module.split("."),
                        __import__(module))

def write_template(name_in, names_out, **kwargs):
    """Write RST-template to file based in values in kwargs."""
    directory = os.path.dirname(__file__)
    basename = "%s.rst.in" % name_in
    for template_dir in conf.templates_path:
        template_dir = os.path.join(directory, template_dir)
        template_file = os.path.join(template_dir, basename)
        if os.path.isfile(template_file): break
    text = codecs.open(template_file, "r", conf.source_encoding).read()
    template = jinja2.Template(text)
    for key, value in kwargs.items():
        underline = "%s_double_underline" % key
        kwargs[underline] = "=" * len(str(value))
        underline = "%s_single_underline" % key
        kwargs[underline] = "-" * len(str(value))
    text = template.render(**kwargs)
    if not text.endswith(("\n", "\r")):
        text = "%s%s" % (text, os.linesep)
    if name_in == "index":
        return codecs.open("index.rst", "w", conf.source_encoding).write(text)
    names_out = list(names_out)
    names_out[-1] = "%s.rst" % names_out[-1]
    path = os.path.join(directory,
                        conf.autogen_output_path,
                        ".".join(names_out))

    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    codecs.open(path, "w", conf.source_encoding).write(text)


if __name__ == "__main__":
    main(sys.argv[1:])
