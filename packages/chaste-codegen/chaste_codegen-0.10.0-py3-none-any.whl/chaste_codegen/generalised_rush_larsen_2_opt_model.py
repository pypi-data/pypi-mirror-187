from chaste_codegen.generalised_rush_larsen_1_opt_model import GeneralisedRushLarsenFirstOrderModelOpt


class GeneralisedRushLarsenSecondOrderModelOpt(GeneralisedRushLarsenFirstOrderModelOpt):
    """ Holds template and information specific for the GeneralisedRushLarsenOpt model type"""

    def __init__(self, model, file_name, **kwargs):
        super().__init__(model, file_name, **kwargs)
        self._templates = ['generalised_rush_larsen_model.hpp', 'generalised_rush_larsen_model_2.cpp']
        self._vars_for_template['model_type'] = 'GeneralizedRushLarsenSecondOrderOpt'
