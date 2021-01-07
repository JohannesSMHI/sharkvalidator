# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-15 14:10

@author: johannes

"""
from sharkvalidator.config import Settings
from sharkvalidator.handler import DataFrames, MultiDeliveries


class App:
    """
    Keep it clean, keep it tidy!
    - read
    - validate
    (- write log) ?
    """
    def __init__(self, *args, **kwargs):
        self.settings = Settings(**kwargs)
        self.deliveries = MultiDeliveries()

    def validate(self, *args, **kwargs):
        """"""
        validator_list = kwargs.get('validator_list') or self.settings.validators_sorted
        for delivery_name in args:
            for validator_name in validator_list:
                validator = self.settings.load_validator(validator_name)
                validator.validate(self.deliveries.select(delivery_name))

    def read(self, *args, **kwargs):
        """"""
        assert 'reader' in kwargs
        assert args

        reader = self.settings.load_reader(kwargs.pop('reader'))
        delivery_name = kwargs.pop('delivery_name')

        reader.load(*args, **kwargs)

        dfs = DataFrames(data_type=reader.get('data_type'))
        for element, item in reader.elements.items():
            df = reader.read_element(item.pop('element_specifier'), **item)
            dfs.append_new_frame(name=element, data=df)

        self.deliveries.append_new_delivery(
            name=delivery_name,
            data=dfs,
        )


if __name__ == '__main__':
    app = App()
    app.read(
        'C:/Temp/DV/validator_test/Hallands kustkontroll kvartal 2_2020.xlsx',
        reader='phyche_xlsx',
        delivery_name='hal_phyche',
    )

    app.read(
        'C:/Temp/DV/validator_test/2020-11-25 1345-2020-LANDSKOD 77-FARTYGSKOD 10',
        reader='phyche_lims',
        delivery_name='lims',
    )

    # app.read(
    #     'C:/Temp/DV/validator_test/PP_DEEP_Phytoplankton_data_2019_2020-05-07.xlsx',
    #     reader='phytop_xlsx',
    #     delivery_name='deep_phyto',
    # )

    # for element, item in app.deliveries['lims'].items():
    #     print(element)
    #     print(item)
