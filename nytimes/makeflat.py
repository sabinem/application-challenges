# -*- coding: utf-8 -*-
"""
This file contains recursive functions that allow
to flatten nested datastructures that are build
with dictionaries and lists

Examples:

{'headline': {'main': 'some headline', 'kicker': 'some excitement'}}
is turned into:
{'headline.main': 'some headline',
'headline.kicker': 'some excitement'}

{'keywords': [{'value': 'US', rank': 1}, {'value': 'Soccer', rank': 2}]}
is tunred into:
{'keywords.0.value': 'US',
 'keywords.0.rank': 1,
 'keywords.1.value': 'Soccer',
 'keywords.1.rank': 2}
```
"""
from collections import OrderedDict


def get_structure_depth(structure):
    """determine the depth of a structure:

    - assume the most complex case and reduce the complexity by 1 degree

    - the structure might be a dictionary or list, in this case the depth is the
    the depth of the nested items + 1

    - catch the case where the depth is 0"""
    if isinstance(structure, dict) and structure:
        return max([get_structure_depth(v) for v in structure.values()]) + 1
    elif isinstance(structure, list) and structure:
        return max([get_structure_depth(v) for v in structure]) + 1
    else:
        return 0


def make_flat_structure(structure):
    """makes a structure flat:

    - if the structure is basic: it is returned as is

    - if the structure is a list or dict,
    a list of tuples is produced:

    struct_items can be [(k,v) for (k,v) in structure.items()]
    if the struture is a dict

    or [('0', l[0]), ('1', l(1)), ...] if the structure is a list

    now values can be made into a flat structure by recursion
    'value_flat_structure' and keys are taken to get the new names,
    which are 'k.key(value_flat_structure)'

    by using an Ordered Dict to flatten the structure, the order
    of values is retained
    - that is especially useful for flattening lists.
    """
    if get_structure_depth(structure) <= 1:
        return structure
    else:
        newdict = OrderedDict()
        struct_items = []
        if isinstance(structure, dict):
            struct_items = structure.items()
        elif isinstance(structure, list):
            struct_items = [(str(structure.index(v)), v) for v in structure]
        for key, value in struct_items:
            if type(value) == dict or type(value) == list:
                flatvalue = make_flat_structure(value)
                if flatvalue:
                    for k, v in flatvalue.items():
                        newkey = key + '.' + k
                        newdict[newkey] = v
            else:
                newdict[key] = value
        return newdict
