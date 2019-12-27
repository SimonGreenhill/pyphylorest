# coding=utf-8
from clldutils.clilib import command, ParserError
from tabulate import tabulate

@command(name='list', usage="list the datasets")
def listdatasets(args):
    rows = []
    for i, ds in enumerate(sorted(args.repos.datasets), 1):
        errors = args.repos.datasets[ds].check()
        rows.append([
            i,
            ds,
            '🗞' if 'paper' not in errors else '',
            '🌿' if 'summary.trees' not in errors else '',
            '🌳' if 'posterior.trees' not in errors else '',
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
        errors = '✅' if not errors else ", ".join(sorted(errors))
        rows.append([ds, errors])
    print(tabulate(rows, headers=['Dataset', 'Errors'], tablefmt="github"))


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
        
    def printchar(p, x, y):
        n = 1
        for i in range(x, y + 1):
            print(i, p, n)
            n += 1
        
        
    if len(args.args) != 1:
        raise ParserError("need an XML filename")
    
    xml = ElementTree.parse(args.args[0])
    
    for treelh in xml.findall(".//distribution[@spec='TreeLikelihood']"):
        data_id = treelh.get('data')
        if data_id:
            # find correct one
            if data_id.startswith("@"):
                data_id = data_id.lstrip("@")
            data = xml.find(".//alignment[@id='%s']/data" % data_id)
            printchar(*get_partition(data))
        else:
            data = treelh.find('./data')  # do we need this?
            datadata = treelh.find('./data/data')
            printchar(*get_partition(datadata))
