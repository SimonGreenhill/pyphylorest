dirs_to_create = ['original', 'nexus', 'paper', 'data']

# files to create
files_to_create = {}
files_to_create['details.txt'] = """
id:
name:
author:
year:
scaling:
reference:
url:
data:
cldf:
"""
files_to_create['notes.txt'] = """
# Notes
"""

files_to_create['taxa.csv'] = "taxon,isocode,glottocode,xd_ids,soc_ids\n"

files_to_create['source.bib'] = ""


def create(repos_path, dataset):
    newdir = repos_path / dataset
    
    if newdir.exists():
        raise IOError("Dataset exists in %s!" % newdir)
        
    newdir.mkdir()
    
    for subdir in dirs_to_create:
        (newdir / subdir).mkdir()
    
    for filename, content in files_to_create.items():
        (newdir / filename).write_text(content, encoding="utf8")
