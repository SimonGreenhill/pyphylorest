from clldutils.clilib import command
from tabulate import tabulate

@command(name='list', usage="list the datasets")  # pragma: no cover
def list(args=None):
    for i, ds in enumerate(sorted(args.repos.datasets), 1):
        print("%3d. %s" % (i, ds))


@command(name='new', usage="creates new dataset")  # pragma: no cover
def new(args=None):
    assert len(args.args) == 1, "need a dataset name"
    from .create import create
    create(args.repos.path, args.args[0])


@command(name='check', usage="checks datasets")  # pragma: no cover
def check(args=None):
    rows = []
    for ds in sorted(args.repos.datasets):
        errors = args.repos.datasets[ds].check()
        if not errors:
            errors = '✅'
        else:
            errors = ", ".join(sorted(errors))
        rows.append([ds, errors])
    print(tabulate(rows, headers=['Dataset', 'Errors'], tablefmt="github"))
