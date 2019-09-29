from clldutils.clilib import command

# TODO new
# TODO summary
@command(name='list', usage="list the datasets")
def list(args=None):
    for i, k in enumerate(sorted(args.repos.datasets), 1):
        print("%3d. %s" % (i, k))


@command(name='new', usage="creates new dataset")
def new(args=None):
    assert len(args) == 1, "need a dataset name"
    from .create import create
    create(args.repos, args[1])
