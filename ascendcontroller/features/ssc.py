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
from math import sqrt
from typing import Sequence, Tuple
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

    def check_speed(self, threshold: float, curr: pandas.Series, prev: pandas.Series) -> Tuple[int, ResultType]:
        if prev is None or curr.sender != prev.sender:
            return (-1, ResultType.Normal.name)
        curr_time = curr['rcvTime']
        prev_time = prev['rcvTime']
        curr_pos = curr['senderPosition']
        prev_pos = prev['rcvTime']
        curr_speed = curr['senderSpeed']
        time_diff = curr_time - prev_time
        dist_diff = distance.euclidean(curr_pos, prev_pos)
        actual_speed = dist_diff / 1 if time_diff == 0 else time_diff  # v = s/t
        last_speed = sqrt(pow(curr_speed[0], 2) + pow(curr_speed[1], 2) + pow(curr_speed[2], 2))
        delta_speed = abs(last_speed - actual_speed)
        return (delta_speed, ResultType.Normal.name if delta_speed > threshold else ResultType.Normal.Attack.name)

    # noinspection PyMethodMayBeStatic

    def process(self, data: pandas.DataFrame) -> FeatureResult:
        params: SscFeatureParam = self.factory.build(data)
        df = params.data

        # Create a index Column
        # df['idx'] = list(range(len(df.index)))

        # Create ssc Columns in the Data Frame
        for threshold in params.thresholds:
            df[f'ssc{threshold}'] = 'Unknown'
        for threshold in params.thresholds:
            df[f'cmtx{threshold}'] = 'Unknown'

        # Sort the Data Frame by Sender Column
        df = df.sort_values('sender', ignore_index=True)

        # Calculate actual speed
        for idx in range(0, len(df)):
            for threshold in params.thresholds:
                curr = df.loc[idx]
                prev = df.loc[idx-1] if idx > 0 else None
                attacker = curr.attackerType.item()
                speed, result = self.check_speed(threshold, curr, prev)
                df.loc[idx, f'speed'] = speed
                df.loc[idx, f'ssc{threshold}'] = result
                df.loc[idx, f'cmtx{threshold}'] = self.confusion_matrix(
                    attacker == 1 or attacker == 2 or attacker == 4 or attacker == 8
                    or attacker == 16, result == ResultType.Attack.name).name

        # Drop unnecessary columns from Data Frame
        df = df.drop(columns=['senderPosition', 'senderSpeed', 'rcvTime'])

        # Return result DataFrame
        return FeatureResult(data=df, prefix='ssc-')
