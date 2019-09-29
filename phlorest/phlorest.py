#!/usr/bin/env python3
# coding=utf-8
import csv
from pathlib import Path


def read_details(path):
    out = {}
    with path.open('r', encoding="utf8") as handle:
        for line in handle:
            if ':' in line:
                k, v = [_.strip() for _ in line.split(":", 1)]
                assert k not in v, 'Duplicate key %s' % k
                out[k] = v
    return out


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
        self.__details, self.__taxa = None, None  # lazy caches
    
    def __repr__(self):
        return '<Phlorest Dataset %s>' % self.details.get('id', '?')
    
    def _get(self, filename):
        if self.details.get(filename):  # override with details
            return self.details.get(filename)
        
        filename = self.dirname / filename
        if not filename.exists():
            return None
        elif filename.is_dir():
            return [x for x in filename.iterdir() if not x.name.startswith(".")]
        else:
            return filename

    @property
    def details(self):
        if not self.__details:
            self.__details = read_details(self.dirname / 'details.txt')
        return self.__details
    
    @property
    def taxa(self):
        if not self.__taxa:
            self.__taxa = read_taxa(self.dirname / 'taxa.csv')
        return self.__taxa
    
    # files
    @property
    def makefile(self):
        return self._get('Makefile').read_text('utf8')

    @property
    def source(self):
        return self._get('source.bib').read_text('utf8')

    @property
    def notes(self):
        return self._get('notes.txt').read_text('utf8')

    # dirs
    @property
    def original(self):
        return self._get('original')
        
    @property
    def paper(self):
        return self._get('paper')

    @property
    def nexus(self):
        return self._get('nexus')

    @property
    def data(self):
        return self._get('data')

    @property
    def cldf(self):
        return self._get('cldf')
    
    # misc
    @property
    def treefiles(self):
        return {
            'summary': self._get("summary.trees"),
            'posterior': self._get("posterior.trees"),
        }

    def check(self):
        raise NotImplementedException('..')
