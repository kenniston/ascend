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

"""
    VeReMi: A Dataset for Comparable Evaluationof Misbehavior Detection 
            in VANETs
    =========================================================================

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

from enum import Enum


class SimulationDensity(Enum):
    LOW = 1,
    MEDIUM = 2,
    HIGH = 3


class AttackType(Enum):
    TYPE1 = 1,
    TYPE2 = 2,
    TYPE4 = 4,
    TYPE8 = 8,
    TYPE16 = 16,


VEHICULAR_LOW_ATTACK1_HIGH = [*range(10, 15)]
VEHICULAR_HIGH_ATTACK1_HIGH = [*range(40, 45)]

VEHICULAR_LOW_ATTACK2_HIGH = [*range(55, 60)]
VEHICULAR_HIGH_ATTACK2_HIGH = [*range(85, 90)]

VEHICULAR_LOW_ATTACK4_HIGH = [*range(100, 105)]
VEHICULAR_HIGH_ATTACK4_HIGH = [*range(130, 135)]

VEHICULAR_LOW_ATTACK8_HIGH = [*range(145, 150)]
VEHICULAR_HIGH_ATTACK8_HIGH = [*range(175, 180)]

VEHICULAR_LOW_ATTACK16_HIGH = [*range(190, 195)]
VEHICULAR_HIGH_ATTACK16_HIGH = [*range(220, 225)]
