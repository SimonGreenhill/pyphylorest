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
            '🌿' if 'summary.trees' not in errors else '',
            '🌳' if 'posterior.trees' not in errors else '',
            '💾' if 'nexus' not in errors else '',
            '💬' if 'data' not in errors else '',
        ])
    headers = headers=['#', 'Dataset', 'mcct', 'posterior', 'nexus', 'data']
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
