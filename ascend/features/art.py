# ---------------------------------------------------------------------------
# ASCEND Framework
#
# Copyright (c) 2011-2022, ASCEND Development Team
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

from abc import ABC
from typing import Sequence, Tuple
import pandas
from scipy.spatial import distance
from ascend.base import Feature, FeatureResult, ResultType, FeatureParam


class ArtFeatureParam(FeatureParam, ABC):
    # List for Acceptance Range Threshold Detector
    thresholds: Sequence[int]
    # Sender vector column names
    svect: Tuple
    # Receiver vector column names
    rvect: Tuple
    # Attacker Type column name
    atype: int


class ArtFeature(Feature):
    def __init__(self, factory: ArtFeatureParam):
        super().__init__(factory=factory)

    # noinspection PyMethodMayBeStatic
    def process(self, data) -> FeatureResult:
        params = self.factory.build(data)
        columns = ['distance'] + list(map(lambda x: f'art{x}', params.thresholds)) + list(
            map(lambda x: f'cmart{x}', params.thresholds))

        # Create Result DataFrame with ART Columns
        data_log = pandas.DataFrame(columns=columns)
        # Check distance between sender and receiver
        dst = distance.euclidean(params.svect, params.rvect)

        # Check confusion matrix for each distance
        art_results = []
        confusion_results = []
        for threshold in params.thresholds:
            # Check for attacks by distance
            result = ResultType.Normal if dst <= threshold else ResultType.Attack
            # Get confusion matrix result
            attacker = params.atype == 1
            detected = result is ResultType.Attack
            confusion = self.confusion_matrix(attacker, detected)
            # Store results
            art_results.append(result.name)
            confusion_results.append(confusion.name)

        # Add row in DataFrame
        data = pandas.DataFrame(
            [[dst] + art_results + confusion_results], columns=columns)
        data_log = pandas.concat([data_log, data], ignore_index=True)
        # Return result DataFrame
        return FeatureResult(data_log)
