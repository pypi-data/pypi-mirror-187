from AoE2ScenarioParser.datasets.support.info_dataset_base import InfoDatasetBase


class SomeC(InfoDatasetBase):
    PLS_DONT_BREAK = 345, -1, -1, 16393, True


print(SomeC.PLS_DONT_BREAK)
