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
from abc import ABC
from typing import Sequence
from scipy.spatial import distance
from ascendcontroller.base import Feature, FeatureResult, ResultType, FeatureParam


class SscFeatureParam(FeatureParam, ABC):
    # List of max speed deviation (m/s) Detector
    thresholds: Sequence[int]


class SscFeature(Feature):
    """
        Required columns in Data Frame:
            - sender                - sender ID
            - senderPosition        - (x, y, z) tuple
            - senderSpeed           - (x, y, z) tuple
            - rcvTime               - Message arrival time
            - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                               4-attack, 8-attack, 16-attack]
    """

    def __init__(self, factory: SscFeatureParam):
        super().__init__(factory=factory)

    # noinspection PyMethodMayBeStatic
    def process(self, data: pandas.DataFrame) -> FeatureResult:
        params: SscFeatureParam = self.factory.build(data)
        df = params.data

        # Create a index Column
        df['idx'] = list(range(len(df.index)))

        # Create ssc Columns in the Data Frame
        for threshold in params.thresholds:
            df[f'ssc{threshold}'] = 'Unknown'
        for threshold in params.thresholds:
            df[f'cmtx{threshold}'] = 'Unknown'

        # Calculate actual speed
        for s in df.sender.unique():
            selection = df[['idx', 'rcvTime', 'senderPosition', 'senderSpeed']].loc[df.sender == s].values.tolist()
            prev = None
            for seq, data in enumerate(selection):
                idx, curr_time, curr_pos, curr_speed = data
                for threshold in params.thresholds:
                    if seq == 0:
                        df.iloc[idx, df.columns.get_loc(f'ssc{threshold}')] = ResultType.Normal.name
                        prev = data
                        continue

                _, prev_time, prev_pos, _ = prev
                time_diff = curr_time - prev_time
                dist_diff = distance.euclidean(curr_pos, prev_pos)
                actual_speed = dist_diff / time_diff  # v = s/t
                delta_speed = abs(curr_speed - actual_speed)
                df.iloc[idx, df.columns.get_loc(
                    f'ssc{threshold}')] = ResultType.Normal.name if delta_speed < threshold else ResultType.Normal.Attack
                prev = data

        # Check confusion matrix for each distance
        for threshold in params.thresholds:
            df[f'cmtx{threshold}'] = df.apply(lambda row: self.confusion_matrix(
                row.attackerType == 1 or row.attackerType == 2 or row.attackerType == 4 or row.attackerType == 8
                or row.attackerType == 16, row[f'ssc{threshold}'] == ResultType.Attack.name).name, axis=1)

        # Return result DataFrame
        return FeatureResult(data=df, prefix='ssc-')
