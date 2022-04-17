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

import os
import re
import pandas
from typing import Sequence
import matplotlib.pyplot as plt
from ascendcontroller.veremi import *
from ascendcontroller.features.art import ArtFeature, ArtFeatureParam
from ascendcontroller.base import CsvRunner, FeatureParam, Feature, FeatureResult


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


class ArtPeformanceResult:
    """ ArtPeformanceResult reads Acceptance Range Threshold and plots a graphs
        with precision and recal values.
    """

    def __init__(self, files: Sequence):
        self.files = files
        self.thresholds = [100, 200, 300, 400, 450, 500, 550, 600, 700, 800]

    def run(self) -> Sequence:
        df = pandas.concat([pandas.read_csv(f) for f in self.files])
        values = {}
        for threshold in self.thresholds:
            # Calculate the precision and recall
            counts = df[f'cmtx{threshold}'].value_counts()
            precision = getattr(counts, 'TP', 0) / (getattr(counts, 'TP', 0) + getattr(counts, 'FP', 0))
            recall = getattr(counts, 'TP', 0) / (getattr(counts, 'TP', 0) + getattr(counts, 'FN', 0))
            values[threshold] = [precision, recall]
        return values


class DmvParam(FeatureParam):
    def build(data: pandas.DataFrame):
        pass


class DmvFeature(Feature):
    def __init__(self, factory: FeatureParam):
        super().__init__(factory)

    def process(self, data: pandas.DataFrame) -> FeatureResult:
        params = self.factory.build(data)
        return FeatureResult()


def process(root_path: str, result_path: str):
    # VeReMi Misbehavior file filter
    file_filter = VEHICULAR_LOW_ATTACK1_HIGH + VEHICULAR_HIGH_ATTACK1_HIGH + \
        VEHICULAR_LOW_ATTACK2_HIGH + VEHICULAR_HIGH_ATTACK2_HIGH + \
        VEHICULAR_LOW_ATTACK4_HIGH + VEHICULAR_HIGH_ATTACK4_HIGH + \
        VEHICULAR_LOW_ATTACK8_HIGH + VEHICULAR_HIGH_ATTACK8_HIGH

    CsvRunner(
        path=root_path,
        destination=result_path,
        features=[ArtFeature(factory=ArtParam)],
        idxfilter=file_filter
    ).process()


def plot_art_result(result_path: str):
    # Process result files
    result_files = [f for f in os.listdir(result_path) if os.path.isfile(f'{result_path}{f}')]

    # Process the Acceptance Range Threshold result for low density
    low_density_indexes = VEHICULAR_LOW_ATTACK1_HIGH
    low_density_files = list(filter(lambda f: int(re.search(r'\d+', f).group()) in low_density_indexes, result_files))
    low_density_files = list(map(lambda f: f'{result_path}{f}', low_density_files))
    low_data = ArtPeformanceResult(files=low_density_files).run()
    low_df = pandas.DataFrame.from_dict(low_data, orient='index', columns=['Precision', 'Recall'])

    high_density_indexes = VEHICULAR_HIGH_ATTACK1_HIGH
    high_density_files = list(filter(lambda f: int(re.search(r'\d+', f).group()) in high_density_indexes, result_files))
    high_density_files = list(map(lambda f: f'{result_path}{f}', high_density_files))
    high_data = ArtPeformanceResult(files=high_density_files).run()
    high_df = pandas.DataFrame.from_dict(high_data, orient='index', columns=['Precision', 'Recall'])

    plt.plot(low_df['Recall'], low_df['Precision'], color='blue', marker='o')
    plt.title('Attacker Type 1 (30.0% Attackers)', fontsize=14)
    plt.xlabel('Recall', fontsize=16)
    plt.ylabel('Precision', fontsize=16)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid(True)
    plt.show()

    plt.plot(high_df['Recall'], high_df['Precision'], color='blue', marker='o')
    plt.title('Attacker Type 1 (30.0% Attackers)', fontsize=14)
    plt.xlabel('Recall', fontsize=16)
    plt.ylabel('Precision', fontsize=16)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    root_path = "/home/kenniston/mestrado-ita/materiais/SBSeg/projetos/dataset-veremi/simulationscsv2"
    result_path = f'{root_path}/result-plausibility/'

    # Process files from root path
    process(root_path, result_path)

    # Calculate result and plot data
    plot_art_result(result_path)
