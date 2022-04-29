# ---------------------------------------------------------------------------
# ASCEND Controller Framework
#
# Copyright (c) 2011-2022, ASCEND Controller Development Team
# Copyright (c) 2011-2022, Open source contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#
#    3. Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ---------------------------------------------------------------------------

import pandas
from ascendcontroller.veremi import *
from ascendcontroller.base import CsvRunner
from ascendcontroller.features.art import ArtFeature, ArtFeatureParam
from ascendcontroller.features.dmv import DmvFeature, DmvFeatureParam
from ascendcontroller.features.ssc import SscFeature, SscFeatureParam
from ascendcontroller.features.saw import SawFeature, SawFeatureParam


class ArtParam(ArtFeatureParam):
    """ ArtFeature requires a specific Data Frame with the following columns:

        - senderPosition        - (x, y, z) tuple
        - receiverPosition      - (x, y, z) tuple
        - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                           4-attack, 8-attack, 16-attack]
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


class DmvParam(DmvFeatureParam):
    """ DmvFeature requires a specific Data Frame with the following columns:

        - sender                - sender ID
        - senderPosition        - (x, y, z) tuple
        - rcvTime               - Message arrival time
        - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                           4-attack, 8-attack, 16-attack]
    """
    def build(data: pandas.DataFrame):
        param = DmvParam()
        # Configure the Thresolds for Distance Moved Verifier
        param.thresholds = [1, 5, 10, 15, 20, 25]

        # Create the required columns for the feature
        data['senderPosition'] = data.apply(lambda row: (row.pxSnd, row.pySnd, row.pzSnd), axis=1)
        data['messageID'] = data.apply(lambda row: int(row.messageID), axis=1)
        data['sender'] = data.apply(lambda row: int(row.sender), axis=1)

        # Drop unnecessary columns from Data Frame
        data = data.drop(columns=['Unnamed: 0', 'sendTime', 'gpsTime', 'pxSnd', 'pySnd',
                                  'pzSnd', 'sxSnd', 'sySnd', 'szSnd', 'pxRcv', 'pyRcv', 'pzRcv',
                                  'sxRcv', 'syRcv', 'szRcv'])

        param.data = data
        return param


class SscParam(SscFeatureParam):
    """ SscFeature requires a specific Data Frame with the following columns:

        - sender                - sender ID
        - senderPosition        - (x, y, z) tuple
        - senderSpeed           - (x, y, z) tuple
        - rcvTime               - Message arrival time
        - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                           4-attack, 8-attack, 16-attack]
    """
    def build(data: pandas.DataFrame):
        param = SscParam()
        # Configure the Thresolds for Distance Moved Verifier
        param.thresholds = [35, 40, 45, 50, 60, 70, 80]  # [5, 10, 15, 20, 30, 40, 50]  # [2.5, 5, 7.5, 10, 15, 20, 25]

        # Create the required columns for the feature
        data['senderPosition'] = data.apply(lambda row: (row.pxSnd, row.pySnd, row.pzSnd), axis=1)
        data['senderSpeed'] = data.apply(lambda row: (row.sxSnd, row.sySnd, row.szSnd), axis=1)
        data['messageID'] = data.apply(lambda row: int(row.messageID), axis=1)
        data['sender'] = data.apply(lambda row: int(row.sender), axis=1)

        # Drop unnecessary columns from Data Frame
        data = data.drop(columns=['Unnamed: 0', 'sendTime', 'gpsTime', 'pxSnd', 'pySnd',
                                  'pzSnd', 'sxSnd', 'sySnd', 'szSnd', 'pxRcv', 'pyRcv', 'pzRcv',
                                  'sxRcv', 'syRcv', 'szRcv'])

        param.data = data
        return param


class SawParam(SawFeatureParam):
    """ SawFeature requires a specific Data Frame with the following columns:

        - senderPosition        - (x, y, z) tuple
        - receiverPosition      - (x, y, z) tuple
        - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                           4-attack, 8-attack, 16-attack]
    """
    def build(data: pandas.DataFrame):
        param = SawParam()
        # Configure the Thresolds for Sudden Appearance Warning
        param.thresholds = [25, 100, 200]

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


def process(root_path: str, result_path: str):
    # VeReMi Misbehavior file filter
    file_filter = VEHICULAR_LOW_ATTACK1_HIGH + VEHICULAR_HIGH_ATTACK1_HIGH + \
        VEHICULAR_LOW_ATTACK2_HIGH + VEHICULAR_HIGH_ATTACK2_HIGH + \
        VEHICULAR_LOW_ATTACK4_HIGH + VEHICULAR_HIGH_ATTACK4_HIGH + \
        VEHICULAR_LOW_ATTACK8_HIGH + VEHICULAR_HIGH_ATTACK8_HIGH

    CsvRunner(
        path=root_path,
        destination=result_path,
        features=[SawFeature(factory=SawParam)],
        idxfilter=file_filter,
        # processes=1,
    ).process()


if __name__ == '__main__':
    root_path = "/home/kenniston/mestrado-ita/materiais/SBSeg/projetos/dataset-veremi/simulationscsv2"
    result_path = f'{root_path}/result-plausibility/'

    # Process files from root path
    process(root_path, result_path)

    # Result for Attacker Type 1
    PeformanceResult.attacker1_result(result_path)
