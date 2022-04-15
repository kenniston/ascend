"""
    ITA Master Degree

    Veremi Plausibility
    ===================
        1. VeReMi: A Dataset for Comparable Evaluationof Misbehavior Detection in VANETs
"""

import pandas
from ascendcontroller.base import CSVRunner, FeatureParam, Feature, FeatureResult
from ascendcontroller.features.art import ArtFeature, ArtFeatureParam
from ascendcontroller.features.common import CommonFeature


class ArtParam(ArtFeatureParam):
    def build(data: pandas.DataFrame):
        param = ArtParam()
        param.thresholds = [100, 200, 300, 400, 450, 500, 550, 600, 700, 800]
        param.svect = (data['pxSnd'], data['pySnd'], data['pzSnd'])
        param.rvect = (data['pxRcv'], data['pyRcv'], data['pzRcv'])
        param.atype = int(data['attackerType'])
        return param


class DMVParam(FeatureParam):
    def build(data: pandas.DataFrame):
        pass


class DMVFeature(Feature):
    def __init__(self, factory: FeatureParam):
        super().__init__(factory)

    def process(self, data) -> FeatureResult:
        params = self.factory.build(data)
        return FeatureResult()


if __name__ == '__main__':
    root_path = "/home/kenniston/mestrado-ita/materiais/SBSeg/projetos/dataset-veremi/simulationscsv2"
    CSVRunner(
        path=root_path,
        destination=f'{root_path}/result-plausibility/',
        features=[CommonFeature(), ArtFeature(factory=ArtParam)],
        processes=1
    ).process()
