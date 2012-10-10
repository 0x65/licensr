from os import path, walk
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from textwrap import dedent
from re import compile, match

import helpers

NEWLINES_AFTER_LICENSE = 2

def _start():
    args = parse_args()
    
    files = get_files(args.path, args.recursive)
    code_files = filter_code_files(files, args.regex)
    license = get_license(args.license)
    preamble = get_preamble(args.preamble)

    if license:
        prepend_commented_text_to_files(code_files, license, epilog='\n'*NEWLINES_AFTER_LICENSE)
    if preamble:
        prepend_commented_text_to_files(code_files, preamble, epilog='\n')


def prepend_commented_text_to_files(files, text, epilog=''):
    for path, file in files:
        commented_text = get_commented_text_for_file(file, text)
        if commented_text:
            prepend_to_file(path.join(path, file), 
                '%s%s' % (commented_text, epilog))


def get_commented_text_for_file(file, text):
    try:
        extension = path.splitext(file)[1][1:]
    except IndexError:
        print "Ignoring file %s - couldn't get the extension of file" % file
        return None

    try:
        comment_rule = helpers.language_comments[extension]
    except KeyError:
        print "Ignoring file %s - don't know how to comment '%s' files" % (file, extension)
        return None

    if comment_rule[0] == helpers.SINGLELINE:
        commented_text = comment_rule[1] + ' ' + text.replace('\n', '\n%s ' % comment_rule[1])
    elif comment_rule[0] == helpers.MULTILINE:
        commented_text = '%s\n%s\n%s' % (comment_rule[1], text, comment_rule[2])
    else:
        raise Exception, 'Malformed comment rule'

    return commented_text


def prepend_to_file(file, text):
    with open(file, 'r+') as f:
        body = f.read()
        if not body.startswith(text):
            f.seek(0)
            f.write(text + body)
    

def get_files(path, recursive):
    files = []
    for dirpath, dirname, filenames in walk(path, topdown=True):
        files.extend([(dirpath, filename) for filename in filenames])
        if not recursive: 
            break
    return files


def filter_code_files(files, regex=None):
    if regex is None:
        regex = r'^[^.].*\.(%s)$' % '|'.join(helpers.language_comments.keys())
    regex = compile(regex)

    return [(path, name) for path, name in files 
           if match(regex, name) is not None]


def get_preamble(preamble):
    if not preamble:
        return None

    if path.exists(preamble):
        with open(preamble, 'r') as f:
            preamble_text = f.read()
        return preamble_text
    else:
        return preamble


def get_license(license):
    if path.exists(license):
        with open(license, 'r') as f:
            text = f.read()
        return text
    elif license == 'gpl3':
        return helpers.gnu_gpl3
    elif license == 'lgpl3':
        return helpers.gnu_lgpl3
    elif license == 'mit':
        return helpers.mit
    elif license == 'apache2':
        return helpers.apache2
    elif license == 'mpl2':
        return helpers.mpl2
    elif license == 'none':
        return None
    else:
        raise Exception, 'Invalid license specified'


def parse_args():
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Adds common licenses to your source files.',
        epilog=dedent('''
            Valid values for `license`:
            ---------------------------
            <file>\t- A file of your own choosing
            gpl3\t- GNU General Public License (GPL), version 3
            lgpl3\t- GNU Lesser General Public License (LGPL), version 3
            apache2\t- Apache License, version 2.0
            mit\t- MIT License
            mpl2\t- Mozilla Public License (MPL), version 2
            none\t- No license is added
        ''')
    )

    arg_parser.add_argument('path', type=str, help='The path root')
    arg_parser.add_argument('license', type=str, help='The license to add')
    arg_parser.add_argument('-r', dest='recursive', action='store_true', 
        help='Recursively traverse directories to add licenses')
    arg_parser.add_argument('-e', dest='regex', type=str,
        help='Regex to specify to which files licenses are added')
    arg_parser.add_argument('-p', dest='preamble', type=str,
        help='A preamble added before the license, either a filename or string \
        (for copyrights, etc.)')

    return arg_parser.parse_args()


if __name__ == '__main__':
    _start()
