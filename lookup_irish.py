#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse

from teanglann import get_teanglann_senses, assign_adjectival_variants


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Lookup English definitions of Irish words from the wonderful "
        "https://www.teanglann.ie/ and https://www.focloir.ie/")

    arg = parser.add_argument
    arg(
        '-v', '--verbose',
        help='List of matching words from foclóir '
        'and full definition from teanglann',
        action='store_true')
    arg(
        'irish-word',
        help="Irish word to look up")
    arg(
        '--focloir-sort', '--foclóir-sort',
        help="Loose ordering of definitions according to importance of GA word on foclóir.ie",
        action='store_true'
    )

    return parser.parse_args(args)
    
def get_definition(sense, GA):
    return_value = "\n"

    return_value += (sense['pos'] or "") + " " + (sense['gender'] or "") + "\n"
    if 'genitive-plural' in sense:
        return_value += sense['genitive-plural'] + "\n"
    if 'verbal-noun' in sense:
        return_value += sense['verbal-noun'] + "\n"
    if 'Adjective' in sense['pos']:
        return_value += assign_adjectival_variants(GA) + "\n"
    return_value += '\n'.join(sense['definitions'])

    print(return_value)
    return return_value

def run_main(args):
    result = ""
    GA = args['irish-word']
    for sense in get_teanglann_senses(GA,
                                      verbose=args['verbose'] if 'verbose' in args else False,
                                      sort_by_foclóir=args['focloir_sort'] if 'focloir_sort' in args else False,
                                      format='bash'):
        print("***************************************************")
        for a in sense:
            print(a + ": " + str(sense[a]))
        print("GA: " + GA)
        print("***************************************************")
        if sense['definitions']:
            result += get_definition(sense, GA)
        return result

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    if args:
        result = run_main(vars(args))
        print(result)
