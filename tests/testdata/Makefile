all: summary.trees posterior.trees data.nex

summary.trees: original/mcelhanon-1967-covarion.mcct.trees
	cp $< $@

posterior.trees: original/mcelhanon-1967-covarion.trees.gz
	nexus_treemanip.py -d 1-10001 $< tmp
	nexus_treemanip.py -t -c -n 1000 tmp $@
	rm tmp

data.nex:
	cp original/mcelhanon-1967.nex $@