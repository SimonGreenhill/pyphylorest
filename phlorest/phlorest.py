#!/usr/bin/env python3
# coding=utf-8
import csv
import logging
from pathlib import Path

import yaml

from nexus import NexusReader

logger = logging.getLogger(__name__)


SCALINGS = [
    None,
    'NA',  # no branch lengths
    'arbitrary', 
    'change',  # parsimony steps
    'substitutions',  # change
    'years',  # years
    'centuries',  # centuries
    'millennia',  # millennia
]


def read_csv(path):
    with path.open('r', encoding="utf8") as handle:
        reader = csv.reader(handle)
        header = False
        for row in reader:
            if not header:
                header = row
            else:
                yield dict(zip(header, row))


class Phlorest:
    def __init__(self, dirname):
        self.dirname = Path(dirname)
        self.logging = logging.getLogger(self.dirname.stem)
        self._details, self._taxa = None, None  # lazy caches
    
    def __repr__(self):
        return '<Phlorest Dataset %s>' % self.details.get('id', '?')
        
    def _get(self, filename):
        filename = self.dirname / filename
        if not filename.exists():
            return None
        elif filename.is_dir():
            return [x for x in filename.iterdir() if not x.name.startswith(".")]
        else:
            return filename

    @property
    def details(self):
        if not self._details:
            with (self.dirname / 'details.txt').open('r', encoding="utf8") as handle:
                self._details = yaml.load(handle, Loader=yaml.FullLoader)
        return self._details
    
    @property
    def taxa(self):
        if not (self.dirname / 'taxa.csv').exists():  # pragma: no cover
            self._taxa = {}
        elif not self._taxa:
            self._taxa = {row['taxon']: row for row in read_csv(self.dirname / 'taxa.csv')}
        return self._taxa
    
    # files
    @property
    def makefile(self):
        return self._get("Makefile")
            
    @property
    def source(self):
        return self._get("source.bib")

    @property
    def notes(self):
        return self._get("notes.txt")

    # dirs
    @property
    def original(self):
        return self._get('original')
        
    @property
    def paper(self):
        return self._get('paper')

    @property
    def nexus(self):
        return self._get("data.nex")

    @property
    def characters(self):
        return self._get('characters.txt')

    @property
    def data(self):
        return self.details.get('data', self._get('data'))

    @property
    def cldf(self):
        return self.details.get('cldf')

    @property
    def summary(self):
        return self._get("summary.trees")

    @property
    def posterior(self):
        return self._get("posterior.trees")
    
    def validate(self):
        # check scaling
        if self.details.get('scaling') not in SCALINGS:
            self.logging.warning(
                "Unknown Scaling '%s'" % self.details.get('scaling')
            )
        if len(self.taxa) == 0:
            self.logging.warning("No taxa defined")
        
        # check trees
        for tf in [self.summary, self.posterior]:
            if tf and tf.exists():
                nex = NexusReader(tf)
                if not nex.trees:
                    self.logging.warning("No trees in %s.%s!" % (self.details.get('id', '?'), tf.stem))
                # are all the taxa in the tree listed in the taxa table?
                unknown = [t for t in nex.trees.taxa if t not in self.taxa]
                if len(unknown):
                    self.logging.warning(
                        "Unknown tips in %s.%s: %r" % (self.details.get('id', '?'), tf.stem, unknown)
                    )
        # if we have characters they should match the nexus
        if self.characters and self.nexus:
            nex = NexusReader(self.nexus)
            if not nex.data:
                self.logging.warning("No data in %s.%s!" % (self.details.get('id', '?'), tf.stem))
            
            
        
    def check(self, validate=False):
        attrs = [
            'makefile', 'source',
            'original', 'paper', 'data',
            'nexus', 'characters',
            'cldf',
            'summary', 'posterior',
        ]
        errors = [a for a in attrs if not getattr(self, a)]
        # special checks
        if not self.details.get('id'):  # empty details
            errors.append("details.txt")
        if not len(self.taxa.keys()):  # no taxa defined
            errors.append("taxa.csv")
        if self.source and len(self.source.read_text()) == 0:
            errors.append("source")  # empty source
        
        if validate:
            self.validate()
        return errors