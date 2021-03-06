#! /usr/bin/env python

import sys,pickle
import os.path

def flatten(tuple_gen,group_col=0,value_col=1):
	'''
	(a,1)(a,2)(b,1) ---> (a,(1,2))(b,1)
	
	Infile must be sorted on group column.
	'''
	group = None
	values = []
	for tup in tuple_gen:
		assert len(tup) == 2, "Tuples must be length 2"
		assert group_col != value_col, "Group and Value columns must be different"
		curr_group = tup[group_col].strip()
		curr_value = tup[value_col].strip()
		if group != curr_group:
			if not group == None: # if not first iteration
				yield group, tuple(values) # yield last group
			group = curr_group
			values = []
		values.append(curr_value)
	yield group, tuple(values)
	
def id_convert(prot_stream,mapping=None):
	'''
	For converting protein ids. Takes a stream of ids and a path to a pickled diciontary
	
	Open mapping (a pickle file).'''
	if mapping == None:
		mapping = "/project/LECA/info_files/all_prot2gene.p"
		assert os.path.exists(mapping), "No file %s" % mapping
	with open(mapping) as f:
		D = pickle.load(f)
		assert type(D) is dict, "Mapping must be pickled dictionary"
	for prot in prot_stream:
		yield D[prot]
		
def stream_2cols(infile,delim=None,header=False):
	'''
	Open a two column file and return a generator of tuples corresponding to the two columns.
	delim: optional delimiter string, default is to split line on whitespace
	header: default is False - if True, skip first line of infile
	'''
	with open(infile) as f:
		if header:
			f.next()
		for line in f:
			if delim:
				line = line.strip().split(delim)
			else:
				line = line.strip().split()
			yield line[0],line[1]

def pickle_2cols(col_stream,pickle_file):
	'''Given an imput stream of length 2 tuples, make dictionary mapping first to second
	element, and pickle the dictionary.'''
	D = {}
	count = 0
	for tup in col_stream:
		D[tup[0]] = tup[1]
		count +=1
	with open(pickle_file,'w') as f:
		pickle.dump(D,f)
	print "Pickled %i lines" % count
	
def taxon_lookup(DB='eggnog'):
	'''Return taxon lookup dictionary'''
	db_taxonPath = {'eggnog':"/project/LECA/eggNOG/info_files/eggnogv4.taxonomies.p",
	'phylomedb':"/project/LECA/eggNOG/info_files/eggnogv4.taxonomies.p",
	'orthomcl':"/project/LECA/eggNOG/info_files/eggnogv4.taxonomies.p"}
	db = DB.lower()
	assert db in db_taxonPath, "Database %s not found" % DB
	taxon_path = db_taxonD[db]
	assert os.path.exists(taxon_path), "No file: %s" % taxon_path
	with open(taxon_path) as f:
		taxonD = pickle.load(f)
	return taxonD
	
if __name__ == '__main__':
	infile = sys.argv[1]
	with open(infile) as f:
		line_gen = (line.strip().split('\t') for line in f)
		for l in flatten(line_gen):
			print l
			