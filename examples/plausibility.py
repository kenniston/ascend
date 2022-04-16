"""
    ITA Master Degree

    Veremi Plausibility
    ===================
        1. VeReMi: A Dataset for Comparable Evaluationof Misbehavior Detection in VANETs

            Files index by Attack Type, vehicular density and attack density.
                =============================================================
                0-44: Type 1 - Constant x=5560, y=5820
                =============================================================
                    low     vehicular | low       attack            [0-4]
                    low     vehicular | medium    attack            [5-9]
                    low     vehicular | high      attack          [10-14]
                    medium  vehicular | low       attack          [15-19]
                    medium  vehicular | medium    attack          [20-24]
                    medium  vehicular | high      attack          [25-29]
                    high    vehicular | low       attack          [30-34]
                    high    vehicular | medium    attack          [35-39]
                    high    vehicular | high      attack          [40-44]
                =============================================================
                45-89: Type 2 - Constante offset Δx=250, Δy=-150
                =============================================================
                    low     vehicular | low       attack          [45-49]
                    low     vehicular | medium    attack          [50-54]
                    low     vehicular | high      attack          [55-59]
                    medium  vehicular | low       attack          [60-64]
                    medium  vehicular | medium    attack          [65-69]
                    medium  vehicular | high      attack          [70-74]
                    high    vehicular | low       attack          [75-79]
                    high    vehicular | medium    attack          [80-84]
                    high    vehicular | high      attack          [85-89]
                =============================================================
                90-134: Type 4 - uniformly random in playground
                =============================================================
                    low     vehicular | low       attack          [90-94]
                    low     vehicular | medium    attack          [95-99]
                    low     vehicular | high      attack        [100-104]
                    medium  vehicular | low       attack        [105-109]
                    medium  vehicular | medium    attack        [110-114]
                    medium  vehicular | high      attack        [115-119]
                    high    vehicular | low       attack        [120-124]
                    high    vehicular | medium    attack        [125-129]
                    high    vehicular | high      attack        [130-134]
                =============================================================
                135-179: Type 8 - Δx,Δy uniformly random from [-300, 300]
                =============================================================
                    low     vehicular | low       attack        [135-139]
                    low     vehicular | medium    attack        [140-144]
                    low     vehicular | high      attack        [145-149]
                    medium  vehicular | low       attack        [150-154]
                    medium  vehicular | medium    attack        [155-159]
                    medium  vehicular | high      attack        [160-164]
                    high    vehicular | low       attack        [165-169]
                    high    vehicular | medium    attack        [170-174]
                    high    vehicular | high      attack        [175-179]
                =============================================================
                180-224: Type 16 - Stop probability += 0.025 each pos update
                =============================================================
                    low     vehicular | low       attack        [180-184]
                    low     vehicular | medium    attack        [185-189]
                    low     vehicular | high      attack        [190-194]
                    medium  vehicular | low       attack        [195-199]
                    medium  vehicular | medium    attack        [200-204]
                    medium  vehicular | high      attack        [205-209]
                    high    vehicular | low       attack        [210-214]
                    high    vehicular | medium    attack        [215-219]
                    high    vehicular | high      attack        [220-224]
                =============================================================

"""

import pandas
from ascendcontroller.base import CSVRunner, FeatureParam, Feature, FeatureResult
from ascendcontroller.features.art import ArtFeature, ArtFeatureParam


class ArtParam(ArtFeatureParam):
    """ ArtFeature requires a specific Data Frame with the following columns:

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
        data = data.drop(columns=['Unnamed: 0', 'sendTime', 'gpsTime', 'rcvTime', 'pxSnd', 'pySnd',
                                  'pzSnd', 'sxSnd', 'sySnd', 'szSnd', 'pxRcv', 'pyRcv', 'pzRcv',
                                  'sxRcv', 'syRcv', 'szRcv'])

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
    filter = [*range(10, 15)] + [*range(40, 45)] + [*range(55, 60)] + \
             [*range(85, 90)] + [*range(100, 105)] + [*range(130, 135)] + \
             [*range(145, 150)] + [*range(175, 180)]
    CSVRunner(
        path=root_path,
        destination=f'{root_path}/result-plausibility/',
        features=[ArtFeature(factory=ArtParam)],
        idxfilter=filter
    ).process()
