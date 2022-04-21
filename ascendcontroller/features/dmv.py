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

import numpy
import pandas
from abc import ABC
from typing import Sequence, Tuple
from scipy.spatial import distance
from ascendcontroller.base import Feature, FeatureResult, ResultType, FeatureParam


class DmvFeatureParam(FeatureParam, ABC):
    # List of min distance for Distance Moved Verifier Detector
    thresholds: Sequence[int]
    time_threshold = 10


class DmvFeature(Feature):
    """
        Required columns in Data Frame:
            - sender                - sender ID
            - senderPosition        - (x, y, z) tuple
            - rcvTime               - Message arrival time
            - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                               4-attack, 8-attack, 16-attack]
    """

    def __init__(self, factory: DmvFeatureParam):
        super().__init__(factory=factory)

    def sender_distance(
        self,
        curr: Tuple[float, float, float],
        prev: Tuple[float, float, float],
        threshold: int
    ) -> ResultType:
        if prev is None:
            return (0, ResultType.Normal.name)
        dist = distance.euclidean(curr, prev)
        result = ResultType.Normal.name if dist > threshold else ResultType.Attack.name
        return (dist, result)

    # noinspection PyMethodMayBeStatic
    def process(self, data: pandas.DataFrame) -> FeatureResult:
        params: DmvFeatureParam = self.factory.build(data)
        df = params.data
        # Create the distance moved column
        df[f'distance'] = 0
        # Create a index Column
        df['idx'] = list(range(len(df.index)))

        # Create DVM Columns in the Data Frame
        for threshold in params.thresholds:
            df[f'dmv{threshold}'] = 'Unknown'
        for threshold in params.thresholds:
            df[f'cmtx{threshold}'] = 'Unknown'

        # Calculate the distance between messages for each sender
        for s in df.sender.unique():
            selection = df[['idx', 'rcvTime', 'senderPosition']].loc[df.sender == s].values.tolist()
            for seq, data in enumerate(selection):
                idx, curr_time, curr_pos = data
                for threshold in params.thresholds:
                    if seq == 0:
                        df.iloc[idx, df.columns.get_loc(f'dmv{threshold}')] = ResultType.Normal.name
                        continue

                    time_diff = 0.0
                    dist = 0.0
                    result = None
                    prev_pos = None
                    counter = 0
                    while counter < len(selection) and time_diff < params.time_threshold and dist < threshold:
                        # Avoid checking itself
                        if selection[counter][0] == idx:
                            break
                        prev_pos = selection[counter][2]
                        dist, result = self.sender_distance(curr_pos, prev_pos, threshold)
                        time_diff = abs(curr_time - selection[counter][1])
                        counter += 1

                    df.iloc[idx, df.columns.get_loc(f'distance')] = dist
                    df.iloc[idx, df.columns.get_loc(f'dmv{threshold}')] = result

        # Check confusion matrix for each distance
        for threshold in params.thresholds:
            df[f'cmtx{threshold}'] = df.apply(lambda row: self.confusion_matrix(
                row.attackerType == 1 or row.attackerType == 2 or row.attackerType == 4 or row.attackerType == 8
                or row.attackerType == 16, row[f'dmv{threshold}'] == ResultType.Attack.name).name, axis=1)

        # Return result DataFrame
        return FeatureResult(data=df, prefix='dmv-')
