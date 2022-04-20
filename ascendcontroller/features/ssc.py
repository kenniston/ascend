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


class SccFeatureParam(FeatureParam, ABC):
    # List of max speed deviation (m/s) Detector
    thresholds: Sequence[int]


class SccFeature(Feature):
    """
        Required columns in Data Frame:
            - sender                - sender ID
            - senderPosition        - (x, y, z) tuple
            - senderPrevPosition    - (x, y, z) tuple
            - rcvTime               - Message arrival time
            - rcvPrevTime           - Message arrival time
            - attackerType          - integer for attack type [0-normal, 1-attack, 2-attack, 
                                                               4-attack, 8-attack, 16-attack]
    """

    def __init__(self, factory: SccFeatureParam):
        super().__init__(factory=factory)

    # noinspection PyMethodMayBeStatic
    def process(self, data: pandas.DataFrame) -> FeatureResult:
        params: SccFeatureParam = self.factory.build(data)
        df = params.data
