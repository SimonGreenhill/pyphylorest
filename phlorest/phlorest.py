#!/usr/bin/env python3
# coding=utf-8
import csv
import logging
from pathlib import Path

import yaml

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


def read_taxa(path):
    out = {}
    with path.open('r', encoding="utf8") as handle:
        reader = csv.reader(handle)
        header = False
        for row in reader:
            if not header:
                header = row
            else:
                row = dict(zip(header, row))
                out[row['taxon']] = row
    return out


class Phlorest:
    def __init__(self, dirname):
        self.dirname = Path(dirname)
        self.logging = logging.getLogger(self.dirname.stem)
        self._details, self._taxa = None, None  # lazy caches
        self._validate()
    
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

    def _validate(self):  # pragma: no cover
        if self.details.get('scaling') not in SCALINGS:
            self.logging.warning(
                "Unknown Scaling '%s'" % self.details.get('scaling')
            )
        if len(self.taxa) == 0:
            self.logging.warning("No taxa defined")
        return True

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
            self._taxa = read_taxa(self.dirname / 'taxa.csv')
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
        return self._get('data')

    @property
    def cldf(self):
        return self.details.get('cldf')

    @property
    def summary(self):
        return self._get("summary.trees")

    @property
    def posterior(self):
        return self._get("posterior.trees")
    
    def check(self):
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
        return errors