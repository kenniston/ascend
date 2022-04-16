"""
    ITA Master Degree

    Veremi Plausibility
    ===================
        1. VeReMi: A Dataset for Comparable Evaluationof Misbehavior Detection in VANETs
"""

import pandas
from ascendcontroller.base import CSVRunner, FeatureParam, Feature, FeatureResult
from ascendcontroller.features.art import ArtFeature, ArtFeatureParam


class ArtParam(ArtFeatureParam):
    """ ArtFeature require a specific DataFrame with following columns:

        - senderPosition        - (x, y, z) tuple
        - receiverPosition      - (x, y, z) tuple
        - attackerType          - integer for attack type [0 - normal, 1 - attack]
    """
    def build(data: pandas.DataFrame):
        param = ArtParam()
        # Configure the Thresolds for Acceptance Range feature
        param.thresholds = [100, 200, 300, 400, 450, 500, 550, 600, 700, 800]

        # Create the required columns for the feature
        data['senderPosition'] = data.apply(lambda row: (row.pxSnd, row.pySnd, row.pzSnd), axis=1)
        data['receiverPosition'] = data.apply(lambda row: (row.pxRcv, row.pyRcv, row.pzRcv), axis=1)
        data['messageID'] = data.apply(lambda row: int(row.messageID), axis=1)
        data['sender'] = data.apply(lambda row: int(row.sender), axis=1)

        # Drop unnecessary columns from Data Frame
        data = data.drop(columns=['sendTime', 'gpsTime', 'rcvTime', 'pxSnd', 'pySnd', 'pzSnd', 'sxSnd',
                                  'sySnd', 'szSnd', 'pxRcv', 'pyRcv', 'pzRcv', 'sxRcv', 'syRcv', 'szRcv'])

        param.data = data
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
        features=[ArtFeature(factory=ArtParam)],
        processes=1
    ).process()
