import gzip
import pandas as pd
from collections import OrderedDict, Callable

class DefaultOrderedDict(OrderedDict):
	# Source: http://stackoverflow.com/a/6190500/562769
	def __init__(self, default_factory=None, *a, **kw):
		if (default_factory is not None and
		   not isinstance(default_factory, Callable)):
			raise TypeError('first argument must be callable')
		OrderedDict.__init__(self, *a, **kw)
		self.default_factory = default_factory

	def __getitem__(self, key):
		try:
			return OrderedDict.__getitem__(self, key)
		except KeyError:
			return self.__missing__(key)

	def __missing__(self, key):
		if self.default_factory is None:
			raise KeyError(key)
		self[key] = value = self.default_factory()
		return value

	def __reduce__(self):
		if self.default_factory is None:
			args = tuple()
		else:
			args = self.default_factory,
		return type(self), args, None, None, self.items()

	def copy(self):
		return self.__copy__()

	def __copy__(self):
		return type(self)(self.default_factory, self)

	def __deepcopy__(self, memo):
		import copy
		return type(self)(self.default_factory,
						  copy.deepcopy(self.items()))

	def __repr__(self):
		return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
											   OrderedDict.__repr__(self))

class VCF():
	def __init__(self, vcf_fn, pheno_fn=None):
		self.vcf_fn = vcf_fn
		self.colnames = self.read_vcf_header(vcf_fn)
		rowdata, data = self.read_vcf(vcf_fn, self.colnames)
		self.rowdata = rowdata
		self.data = data
		if pheno_fn != None:
			coldata = self.read_phenotype(pheno_fn, self.data.columns)
			self.coldata = coldata


	def read_vcf_header(self, vcf_fn):
		if ".gz" in vcf_fn:
			with gzip.open(vcf_fn, "r") as f:
				for line in f:
					line = line.decode("utf-8").strip()
					if line.startswith("#CHROM"):
						split_line = line.split("\t")
						split_line[0] = "CHROM"
		else:
			with open(vcf_fn, "r") as f:
				for line in f:
					line = line.strip()
					if line.startswith("#CHROM"):
						split_line = line.split("\t")
						split_line[0] = "CHROM"
		return split_line


	def read_vcf(self, vcf_fn, colnames):
		vcf = pd.read_table(vcf_fn, comment="#", header=None, names=colnames)
		rowdata = vcf[['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']]
		data = vcf.iloc[:,9:]
		return rowdata, data


	def read_phenotype(self, pheno_fn, sample):
		pheno = pd.read_table(pheno_fn)
		pheno = pheno[pheno["Accession ID"].isin(sample)]
		pheno.set_index("Accession ID", inplace=True)
		pheno = pheno.reindex(sample)
		pheno.reset_index(inplace=True)
		pheno.rename(columns={"index":"Accession ID"}, inplace=True)
		return pheno


	def __repr__(self):
		return f"VCF: {self.vcf_fn}\nNumber of samples: {self.data.shape[1]}\nNumber of sites: {self.data.shape[0]}"

