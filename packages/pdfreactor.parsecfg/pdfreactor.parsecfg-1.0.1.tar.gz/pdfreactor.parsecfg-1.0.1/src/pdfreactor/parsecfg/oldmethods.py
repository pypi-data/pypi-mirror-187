"""
oldmethods: Map old API method calls (i.e., their arguments) to config keys of
the new PDFreactor client API,
and provide a conversion function.

As far as "symbols" are involved (like CLEANUP_CYBERNEKO and the like), we
have a mapping of the old names to the new values already in ./oldsymbols.py.

We'll use a little test helper function:

    >>> from pdfreactor.parsecfg.convert import parse_configuration
    >>> def om(cfgtext):
    ...     config = parse_configuration(cfgtext, convert=convert_api_method)
    ...     return sorted(config.items())

We have basic knowledge about the methods signatures:

    >>> om('enableDebugMode(on)')
    Traceback (most recent call last):
      ...
    ValueError: enableDebugMode() doesn't accept any arguments! (<NAME on>)

Without arguments, enableDebugMode() will work:

    >>> om('enableDebugMode();setAddLinks(yes)')
    ... # doctest: +NORMALIZE_WHITESPACE
    [('debugSettings', {'appendLogs': True}),
     ('disableLinks',    False)]

Old and new style can be combined:

    >>> om('debugSettings.attachConfiguration=on;enableDebugMode()')
    ... # doctest: +NORMALIZE_WHITESPACE
    [('debugSettings', {'attachConfiguration': True,
                        'appendLogs': True})]

Her a real-world example, including comments:

    >>> om('''
    ... setEncoding('UTF-8')
    ... setJavaScriptMode(JAVASCRIPT_MODE_ENABLED)
    ... # Enable bookmarks in the PDF document
    ... setAddBookmarks(True)
    ... setCleanupTool(CLEANUP_NONE)
    ... setLogLevel(LOG_LEVEL_INFO)
    ... setAppendLog(off)
    ... setDocumentType(DOCTYPE_HTML5)
    ... ''') # doctest: +NORMALIZE_WHITESPACE
    [('addBookmarks', True),
     ('cleanupTool', 'NONE'),
     ('debugSettings', {'appendLogs': False}),
     ('documentType', 'HTML5'),
     ('encoding', 'UTF-8'),
     ('javaScriptMode', 'ENABLED'),
     ('logLevel', 'INFO')]

NOTE:
    There has been a change in the symbols which have been provided for such
    calls; the CLEANUP_NONE symbol, to take one, was "renamed" to Cleanup.NONE
    (there is a 'Cleanup' attribute now to the PDFreactor class, which is a
    mini class itself and provides some names).
    The values have changed as well; while they used to be numeric, they are
    now strings, usually containing a trailing part of the name.

    There is no transformation of such values yet!

But what we have is a transformation of old to new symbols:

    >>> om('setJavaScriptMode(JAVASCRIPT_MODE_ENABLED_NO_LAYOUT)')
    [('javaScriptMode', 'ENABLED_NO_LAYOUT')]

Our old-to-new-symbols mapping looks quite reasonable already,
but our methods information is not equally complete yet;
thus, this won't work:

    >>> om('setConformance(CONFORMANCE_PDFA)')  # doctest: +SKIP

Some metthos add to a list:

    >>> om("addUserScript('ro.layout.forceRelayout();', Null, False)")
    ...                               # doctest: +NORMALIZE_WHITESPACE
    [('userScripts', [{'content': 'ro.layout.forceRelayout();',
                       'beforeDocumentScripts': False,
                       'uri': None}])]


Contributions are welcome.
"""

# Python compatibility:
from __future__ import absolute_import, print_function

# Standard library:
from tokenize import NAME

__all__ = [
        'convert_api_method',
        ]

# Local imports:
from pdfreactor.parsecfg.convert import resolve_value
from pdfreactor.parsecfg.oldsymbols import OLD2NEW
from pdfreactor.parsecfg.symbols import SYMBOL_STRINGS


def negate(val):
    # negate the given value
    return not val

def unsupported(val):
    raise ValueError('The use of this method can\'t be converted '
                     'to some config key in the new PDFreactor API!')


_MAP2 = {
    # no arguments --> one dict:
    'enableDebugMode': {
        'key': 'debugSettings',
        'subkey': 'appendLogs',
        'value': True,
        },
    # ... but usually we have arguments:
    'setOutputFormat': [{
        'key': 'outputType',
        'subkey': 'type',
        }, {
        'key': 'outputType',
        'subkey': 'width',
        }, {
        'key': 'outputType',
        'subkey': 'height',
        }],
    'setCleanupTool': [{  # _new.Cleanup symbols
        'key': 'cleanupTool',
        }],
    'setEncoding': [{
        'key': 'encoding',
        }],
    'setJavaScriptMode': [{  # _new.JavaScriptMode symbols
        'key': 'javaScriptMode',
        }],
    'setAddBookmarks': [{
        'key': 'addBookmarks',
        }],
    'setAddLinks': [{
        'key': 'disableLinks',
        'convert': negate,
        }],
    'setAppendLog': [{
        'key': 'debugSettings',
        'subkey': 'appendLogs',
        }],
    'setDocumentType': [{
        'key': 'documentType',
        }],
    'setLicenseKey': [{  # not to be confused with the PDFreactor.apiKey attribute!
        'key': 'licenseKey',
        }],
    # https://www.pdfreactor.com/product/doc_html/#Logging
    'setLogLevel': [{  # _new.logLevel symbols
        'key': 'logLevel',
        }],
    # some methods add to a list:
    'addUserScript': {
        'key': 'userScripts',
        'model': [{
            'subkey': 'content',
            }, {
            'subkey': 'uri',
            }, {
            'subkey': 'beforeDocumentScripts',
            }],
        },
    }


def _specs(liz):
    if not liz:
        return
    elif not liz[1:]:
        yield 'val'
        return
    res = []
    for dic in liz:
        yield dic['subkey']


def convert_api_method(statement, config, control):  #  [[
    """
    Convert API methods (which are not used in the Python client API anymore)
    in config key assigments.

    Since this function is used as a `convert` argument to the
    parse_configuration function, we need to have a config and control dict,
    and we'll return a boolean value.

    >>> from pdfreactor.parsecfg.parse import generate_statements
    >>> def first_stmt(txt):
    ...     return list(generate_statements(txt))[0]
    >>> config = {}
    >>> ctrl = {}
    >>> stmt = first_stmt('the_answer=41')
    >>> convert_api_method(stmt, config, ctrl)
    False

    Well, this function doesn't convert assignments;
    so it returns False to allow you to try something else.

    For our further tests, we'll use a little test helper:
    >>> def cvt(txt, which='config'):
    ...     config = {}
    ...     control = {}
    ...     for stmt in generate_statements(txt):
    ...         res = convert_api_method(stmt, config, control)
    ...         print(res)
    ...     if which in ('config', 'both'):
    ...         print(sorted(config.items()))
    ...     if which in ('control', 'both'):
    ...         print(sorted(control.items()))

    >>> cvt('setAddLinks(yes)')
    True
    [('disableLinks', False)]

    >>> cvt('enableDebugMode()')
    True
    [('debugSettings', {'appendLogs': True})]

    """
    if not statement.is_method_call:
        return False

    grp0 = statement[0]
    the_name = grp0.dotted_name

    if the_name not in _MAP2:
        return False
    info = _MAP2[the_name]

    model = None  # for lists
    make_list = False
    if isinstance(info, dict):
        model = info.get('model')
        if model:
            make_list = True
        no_args = not model
    else:
        no_args = False

    if no_args:  # e.g. enableDebugMode
        if statement.method_args:
            too_much = statement.method_args[0]
            elli = ('[...]' if statement.method_args[1:]
                    else '')
            raise ValueError('%(the_name)s() doesn\'t accept any arguments!'
                    ' (%(too_much)s%(elli)s)'
                    % locals())
        subkey = info.get('subkey')
        key = info['key']
        value = info['value']
        if subkey is None:
            config[key] = value
        else:
            config.setdefault(key, {})
            config[key][subkey] = value
        return True

    args = statement.method_args
    # the method call might be invalid;
    # currently it is more likely for us not to support it yet ...
    if model is not None:
        if len(args) > len(model):
            return False
    else:
        if len(args) > len(info):
            return False
    i = 0

    if make_list:  # e.g. addUserScript
        key = info['key']
        config.setdefault(key, [])
        the_list = config[key]
        the_dict = None
        have_unnamed = False
        done = False

        for valgrp in args:
            if valgrp.ttype == NAME:
                name = valgrp.dotted_name
                if name in OLD2NEW:
                    name = OLD2NEW[name]
                    val = SYMBOL_STRINGS[name]
                elif name in SYMBOL_STRINGS:
                    val = SYMBOL_STRINGS[name]
                else:
                    val = resolve_value(valgrp)
            else:
                val = resolve_value(valgrp)
            nfo = model[i]
            convert = nfo.get('convert')
            if convert is not None:
                val = convert(val)
            subkey = nfo.get('subkey')
            if subkey is None:
                if i != 0:
                    raise ValueError('%(the_name)s(): for multiple arguments '
                            "we'd expect to have subkeys, right?"
                            ' (#%(i)d: %(valgrp)r; %(nfo)r)'
                            % locals())
                the_list.append(val)
                config[key] = val
                done = True
            elif done:
                raise ValueError('%(the_name)s(): for multiple arguments '
                        "we'd expect to have subkeys FOR ALL, right?"
                        ' (#%(i)d: %(valgrp)r; %(nfo)r)'
                        % locals())
            else:
                if the_dict is None:
                    the_dict = {}
                elif subkey in the_dict:
                    oldval = the_dict[subkey]
                    raise ValueError('%(the_name)s(): multiple values '
                            'for subkey %(subkey)r (%(oldval)r, %(val)r)'
                            % locals())

                the_dict[subkey] = val
            i += 1
        if not done:
            the_list.append(the_dict)
	return True

    for valgrp in args:
        if valgrp.ttype == NAME:
            name = valgrp.dotted_name
            if name in OLD2NEW:
                name = OLD2NEW[name]
                val = SYMBOL_STRINGS[name]
            elif name in SYMBOL_STRINGS:
                val = SYMBOL_STRINGS[name]
            else:
                val = resolve_value(valgrp)
        else:
            val = resolve_value(valgrp)
        nfo = info[i]
        convert = nfo.get('convert')
        if convert is not None:
            val = convert(val)
        subkey = nfo.get('subkey')
        key = nfo['key']
        if subkey is None:
            config[key] = val
        else:
            config.setdefault(key, {})
            config[key][subkey] = val
        i += 1
    return True


if __name__ == '__main__':
  # (further development code removed)
  if 0:
    # Python compatibility:
    from six.moves import zip

    dictnames = set()
    nodicts = set()

    for name in sorted(_MAP2.keys()):
        args = _MAP2[name]
        specs = list(_specs(args))
        arglist = ', '.join(specs)
        print('%(name)s(%(arglist)s) -->' % locals())
        for spec, dic in zip(specs, args):
            try:
                key = dic['key']
            except KeyError:
                print('    (UNSUPPORTED)')
            else:
                if dic.get('convert'):
                    spec = '(converted) ' + spec
                if 'subkey' in dic:
                    subkey = dic['subkey']
                    assert key not in nodicts
                    dictnames.add(key)
                    print('    config[%(key)r][%(subkey)r] = %(spec)s' % locals())
                else:
                    assert key not in dictnames
                    nodicts.add(key)
                    print('    config[%(key)r] = %(spec)s' % locals())
  else:
    # Standard library:
    import doctest
    doctest.testmod()
