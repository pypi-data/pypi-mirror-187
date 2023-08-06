import abc
import numpy as np
from typing import Union

from cobamp.wrappers import available_readers_dict, get_model_reader
from cobamp.wrappers.core import AbstractObjectReader

from troppo.methods.reconstruction.fastcore import FASTcore, FastcoreProperties
from troppo.methods.reconstruction.gimme import GIMME, GIMMEProperties
from troppo.methods.reconstruction.imat import IMAT, IMATProperties
from troppo.methods.reconstruction.corda import CORDA, CORDAProperties
from troppo.methods.reconstruction.tINIT import tINIT, tINITProperties
from troppo.methods.reconstruction.swiftcore import SWIFTCORE, SwiftcoreProperties

from .methods.gapfill.efm import EFMGapfill, EFMGapfillProperties

from .omics.core import OmicsContainer

from .omics.integration import *

map_properties_algorithms = {
	FastcoreProperties : FASTcore,
	GIMMEProperties : GIMME,
	IMATProperties : IMAT,
	tINITProperties : tINIT,
	CORDAProperties : CORDA,
	SwiftcoreProperties: SWIFTCORE
}

algorithm_instance_map = {
	'fastcore': FASTcore,
	'gimme': GIMME,
	'imat': IMAT,
	'tinit': tINIT,
	'corda': CORDA,
	'swiftcore': SWIFTCORE
}

integration_strategy_map = {
	'continuous': ContinuousScoreIntegrationStrategy,
	'custom': CustomSelectionIntegrationStrategy,
	'threshold': ThresholdSelectionIntegrationStrategy,
	'default_core': DefaultCoreIntegrationStrategy,
	'adjusted_score': AdjustedScoreIntegrationStrategy
}

ao_function_pair_map = {
	'minmax': MINMAX,
	'minsum': MINSUM
}

gapfill_algorithm_map = {
	'efm': EFMGapfill
}

gapfill_properties_map = {
	EFMGapfillProperties: EFMGapfill
}

class ModelBasedWrapper(object):
	__metaclass__ = abc.ABCMeta
	def __init__(self, model, **kwargs):
		self.__model = model
		if model.__module__ in available_readers_dict.keys():
			self.model_reader = get_model_reader(model, **kwargs)
		elif isinstance(model, AbstractObjectReader):
			self.model_reader = model
		else:
			raise TypeError(
				"The `model` instance is not currently supported by cobamp. Currently available readers are: " + str(
					list(available_readers_dict.keys())))
		self.S = self.model_reader.get_stoichiometric_matrix()
		self.lb, self.ub  = [np.array(bounds) for bounds in self.model_reader.get_model_bounds(False, True)]

	@property
	def original_model_instance(self):
		return self.__model

		# ...
class GapfillWrapper(ModelBasedWrapper):
	def run(self, avbl_fluxes, algorithm, ls_override=None, **kwargs):
		if ls_override is None:
			ls_override = {}

		rx_map, mt_map = [{v:k for k,v in dict(enumerate(l)).items()} for l in
		          [self.model_reader.r_ids, self.model_reader.m_ids]]

		algo_class = gapfill_algorithm_map[algorithm]
		algo_props = algo_class.properties_class
		prop_kwargs = {'avbl_fluxes': avbl_fluxes, 'lsystem_args': ls_override}
		prop_kwargs.update(**kwargs)

		decoders = algo_props.decoder_functions
		prop_kwargs = {k: decoders[k](v, rx_map, mt_map) if k in decoders.keys() else v
		               for k, v in prop_kwargs.items()}
		algo_props_inst = algo_props(**prop_kwargs)

		algo_inst = algo_class(self.S, self.lb, self.ub, algo_props_inst)
		# if isinstance(avbl_fluxes[0], (str,int)):
		res = algo_inst.run()
		# else:
		# 	avbl_flux_list = [decoders['avbl_fluxes'](v, rx_map, mt_map) for v in avbl_fluxes]
		# 	res = algo_inst.batch_run(avbl_flux_list)

		return [[self.model_reader.r_ids[k] for k in s] for s in res]


class ReconstructionWrapper(ModelBasedWrapper):
	def run(self, properties):
		algo = map_properties_algorithms[type(properties)](self.S, self.lb, self.ub, properties)
		return algo.run()

	def run_from_omics(self, omics_data: Union[dict,list,tuple,OmicsContainer], algorithm, integration_strategy,
	                   and_or_funcs=(min, max), raise_errors=True,**kwargs):
		def tuple_to_strat(x):
			return integration_strategy_map[x[0]](x[1])

		ordered_ids = {r:i for i,r in enumerate(self.model_reader.r_ids)}
		afx, ofx = 	and_or_funcs
		strat = tuple_to_strat(integration_strategy) \
			if isinstance(integration_strategy, (list, tuple)) else integration_strategy
		if isinstance(omics_data, OmicsContainer):
			scores = strat.integrate(omics_data.get_integrated_data_map(self.model_reader, afx, ofx))
		elif isinstance(omics_data, (dict, list, tuple)):
			scores = omics_data
		else:
			raise TypeError('omics_data must be an OmicsContainer instance, a dict[str,Number] or an tuple/list with'+\
			                'reactions')
		if isinstance(scores, dict):
			res = [scores[k] for k in self.model_reader.r_ids]
		else:
			if isinstance(scores, (tuple, list)) and len(scores) > 0:
				res = [[ordered_ids[k] for k in l] for l in scores]
			else:
				res = [ordered_ids[k] for k in scores]

		properties = algorithm_instance_map[algorithm].properties_class.from_integrated_scores(res, **kwargs)

		try:
			algorithm_result = self.run(properties)
			result_names =  [self.model_reader.r_ids[k] for k in algorithm_result]
			return {k: k in result_names for k in self.model_reader.r_ids}
		except Exception as e:
			print('Model reconstruction failed with exception:',e)
			if raise_errors:
				raise e
			else:
				return {r: False for r in self.model_reader.r_ids}