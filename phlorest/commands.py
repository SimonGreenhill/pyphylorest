# coding=utf-8
import warnings
from pathlib import Path
from textwrap import dedent
from clldutils.clilib import command, ParserError
from tabulate import tabulate

CHECKMARK = '✅'
ERROR = '❌'

@command(name='list', usage="list the datasets")
def listdatasets(args):
    rows = []
    for i, ds in enumerate(sorted(args.repos.datasets), 1):
        errors = args.repos.datasets[ds].check()
        rows.append([
            i,
            ds,
            '🗞' if 'paper' not in errors else '',
            '🌿' if 'summary' not in errors else '',
            '🌳' if 'posterior' not in errors else '',
            '💾' if 'nexus' not in errors else '',
            '🏷' if 'characters' not in errors else '',
            '💬' if 'data' not in errors else '',
            'CLDF' if 'cldf' not in errors else '',
            '🎈' if 'source' not in errors else '',
        ])
    headers = headers=['#', 'Dataset', 'Paper', 'Tree', 'Post.', 'Nex', 'Chars', 'Data', 'CLDF', 'Bib']
    print(tabulate(rows, headers=headers, tablefmt="github"))


@command(name='new', usage="creates new dataset")
def new(args):
    if len(args.args) != 1:
        raise ParserError("need a dataset name")
    from .create import create
    create(args.repos.path, args.args[0])


@command(name='check', usage="checks datasets")
def check(args):
    rows = []
    for ds in sorted(args.repos.datasets):
        errors = args.repos.datasets[ds].check()
        errors = CHECKMARK if not errors else ", ".join(sorted(errors))
        rows.append([ds, errors])
    print(tabulate(rows, headers=['Dataset', 'Errors'], tablefmt="github"))


@command(name='validate', usage="runs validation")
def validate(args):
    for ds in sorted(args.repos.datasets):
        with warnings.catch_warnings(record=True) as warned:
            warnings.simplefilter("always")
            args.repos.datasets[ds].validate()
            if not warned:
                print("%s %s" % (CHECKMARK, ds))
            else:
                print("%s %s" % (ERROR, ds))
                for w in warned:
                    print("\t%s" % w.message)
                print()
            


@command(name='dplace', usage="prints out DPLACE index.csv information")
def dplace(args):
    import sys, csv
    
    if len(args.args) != 1:
        raise ParserError("need a dataset name")
    
    ds = args.repos.datasets.get(args.args[0])
    assert ds is not None, "Unknown dataset %s" % args.args[0]
    writer = csv.writer(sys.stdout)
    writer.writerow(['id', 'name', 'author', 'year', 'scaling', 'reference', 'url'])
    writer.writerow([
        ds.details.get('id', ''),
        ds.details.get('name', ''),
        ds.details.get('author', ''),
        ds.details.get('year', ''),
        ds.details.get('scaling', ''),
        ds.details.get('reference', ''),
        ds.details.get('url', ''),
    ])


@command(name='beast2chars', usage="prints out a character block from a beast2 XML file")
def beast2chars(args):
    import xml.etree.ElementTree as ElementTree

    def find_filter(node):  # note recursive
        for child in node:
            find_filter(child)
            (p, x, y) = get_partition(node)
            if p and x and y:
                return (p, x, y)

    def get_partition(p):
        x, y = [int(_) for _ in p.get('filter').split("-")]
        return (p.get('id'), x, y)
        
    def printchar(p, x, y, ascertained=False):
        n = 1
        for i in range(x, y + 1):
            label = "%s-%s" % (p, 'ascertained' if n == 1 and ascertained else str(n))
            print(i, label)
            n += 1
    
    def get_by_id(data_id):
        if data_id.startswith("@"):
            data_id = data_id.lstrip("@")
        return xml.find(".//alignment[@id='%s']" % data_id)
        
    
    if len(args.args) != 1:
        raise ParserError("need an XML filename")
    
    xml = ElementTree.parse(args.args[0])
    
    for treelh in xml.findall(".//distribution[@spec='TreeLikelihood']"):
        if treelh.get('data'):
            data = get_by_id(treelh.get('data'))
            ascertained = data.get('ascertained') == 'true'
            printchar(*get_partition(data.find('./data')), ascertained=ascertained)
        else:
            data = treelh.find('./data')
            ascertained = data.get('ascertained') == 'true'
            if data.get('data'):
                datadata = get_by_id(data.get('data'))
            else:
                datadata = treelh.find('./data/data')
            printchar(*get_partition(datadata), ascertained=ascertained)


@command(name='itemise', usage="lists all the values for a given item")
def itemise(args):
    if len(args.args) != 1:
        raise ParserError("need a value to itemise")
    
    for ds in sorted(args.repos.datasets):
        d = args.repos.datasets[ds]
        
        try:
            dvalue = getattr(d, args.args[0])
        except AttributeError:
            dvalue = d.details.get(args.args[0], None)
            
        print("%s = %s" % (ds.ljust(40), dvalue))



@command(name='readme', usage="makes a readme.md file")
def readme(args):
    if len(args.args) != 1:
        raise ParserError("need a dataset name")
    
    def fmt(x):
        template = "[%(var)s](%(var)s)"
        if x is None:  # pragma: no cover
            return None
        elif isinstance(x, Path):
            return template % {'var': x.relative_to(ds.dirname)}
        else:
            return template % {'var': x}
    
    ds = args.repos.datasets.get(args.args[0])
    assert ds is not None, "Unknown dataset %s" % args.args[0]
    
    nchar = ""
    if ds.characters:
        nchar = "%d characters - " % len(ds.characters.read_text().split("\n"))
    
    print(dedent(f"""\
    # {ds.details['name']}:
    
    ```
    {ds.details['reference']}
    ```
    
    * ID: {ds.details['id']}:
    * URL: {fmt(ds.details['url'])}
    * Paper: {fmt(ds.dirname / 'paper')}
    * Original Files: {fmt(ds.dirname / 'original')}
    * Scaling: {ds.details['scaling']}
    * Taxa: {len(ds.taxa)} taxa 
    * Data: {fmt(ds.dirname / 'data')}
    * Nexus: {fmt(ds.nexus)}
    * Character Specification: {nchar}{fmt(ds.characters)}
    * Summary Tree: {fmt(ds.summary)}
    * Posterior Probability Distribution: {fmt(ds.posterior)}
    
    ## Errors:
    """))
    
    for e in ds.check():  # pragma: no cover
        print("* missing %s" % e)
    
