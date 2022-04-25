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

import os
import re
import pandas
from enum import Enum
from matplotlib import pyplot as plt
from typing import Dict, Sequence, Tuple


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


class ChartFeature(Enum):
    ART = 1,
    SAW = 2.
    SSC = 3,
    DMV = 4


LineChartData = Tuple[pandas.DataFrame, str]
LineChartVector = Sequence[LineChartData]
LineChartDict = Dict[SimulationDensity, LineChartVector]


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


class PeformanceResult:
    """ PeformanceResult read results and plots a graphs with precision 
        and recal values.

        PeformanceResult requires a specific Data Frame with the following columns:

        - cmtx[XXX]             - [XXX] is the number of Threshold in each algorithm (ART, SAW, SSC and DMV)
                                        and the values for each type can be TP, FP, TN and FN.
    """
    thresholds = [100, 200, 300, 400, 450, 500, 550, 600, 700, 800]
    thresholds_saw = [25, 100, 200]
    thresholds_ssc = [5, 10, 15, 20, 30, 40, 50]  # [2.5, 5, 7.5, 10, 15, 20, 25]
    thresholds_dmv = [1, 5, 10, 15, 20, 25]

    @staticmethod
    def run(ctype: ChartFeature, files: Sequence) -> Sequence:
        df = pandas.concat([pandas.read_csv(f) for f in files])
        values = {}
        lst = None
        if ctype is ChartFeature.ART:
            lst = PeformanceResult.thresholds
        elif ctype is ChartFeature.SAW:
            lst = PeformanceResult.thresholds_saw
        elif ctype is ChartFeature.SSC:
            lst = PeformanceResult.thresholds_ssc
        elif ctype is ChartFeature.DMV:
            lst = PeformanceResult.thresholds_dmv

        for threshold in lst:
            # Calculate the precision and recall
            counts = df[f'cmtx{threshold}'].value_counts()
            precision = getattr(counts, 'TP', 0) / (getattr(counts, 'TP', 0) + getattr(counts, 'FP', 0))
            recall = getattr(counts, 'TP', 0) / (getattr(counts, 'TP', 0) + getattr(counts, 'FN', 0))
            values[threshold] = [precision, recall]

        return values

    @staticmethod
    def get_result_data(
        result_path: str,
        fl: str,
        fh: str,
        lowidx: Sequence,
        highidx: Sequence,
        ctype: ChartFeature
    ) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
        low_df = None if not os.path.exists(f'{result_path}{fl}') else pandas.read_csv(f'{result_path}{fl}')
        high_df = None if not os.path.exists(f'{result_path}{fh}') else \
            pandas.read_csv(f'{result_path}{fh}')

        if high_df is None or low_df is None:
            # Process result files
            result_files = [f for f in os.listdir(result_path) if os.path.isfile(f'{result_path}{f}')]

            # Process the results for LOW density
            low_density_indexes = lowidx
            low_density_files = list(filter(lambda f: int(re.search(r'\d+', f).group())
                                            in low_density_indexes, result_files))
            low_density_files = list(map(lambda f: f'{result_path}{f}', low_density_files))
            low_data = PeformanceResult.run(ctype=ctype, files=low_density_files)
            low_df = pandas.DataFrame.from_dict(low_data, orient='index', columns=['Precision', 'Recall'])
            low_df.to_csv(f'{result_path}{fl}', index_label='Distance')
            low_df['Distance'] = list(low_data.keys())
            low_df = low_df.reset_index(drop=True)

            # Process the results for HIGH density
            high_density_indexes = highidx
            high_density_files = list(filter(lambda f: int(re.search(r'\d+', f).group())
                                             in high_density_indexes, result_files))
            high_density_files = list(map(lambda f: f'{result_path}{f}', high_density_files))
            high_data = PeformanceResult.run(ctype=ctype, files=high_density_files)
            high_df = pandas.DataFrame.from_dict(high_data, orient='index', columns=['Precision', 'Recall'])
            high_df.to_csv(f'{result_path}{fh}', index_label='Distance')
            high_df['Distance'] = list(high_data.keys())
            high_df = high_df.reset_index(drop=True)

        return (low_df, high_df)

    @staticmethod
    def plot(
        data: LineChartDict,
        title1: str,
        title2: str
    ):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 6))
        ax1.set_title(title1, fontsize=14)
        ax1.set_xlabel(xlabel='Recall', fontsize=16, labelpad=40)
        ax1.set_ylabel(ylabel='Precision', fontsize=16, labelpad=30)
        ax1.set_xlim([0, 1])
        ax1.set_ylim([0, 1])
        ax1.grid(True)

        ax2.set_title(title2, fontsize=14)
        ax2.set_xlabel(xlabel='Recall', fontsize=16, labelpad=40)
        ax2.set_ylabel(ylabel='Precision', fontsize=16, labelpad=30)
        ax2.set_xlim([0, 1])
        ax2.set_ylim([0, 1])
        ax2.grid(True)

        for density, cdata in data.items():
            if density is SimulationDensity.LOW:
                for df, color in cdata:
                    if df.empty:
                        continue
                    ax1.plot(df['Recall'], df['Precision'], color=color, marker='o')
                    fpos = (df.Recall[0], df.Precision[0])
                    ax1.annotate(
                        df.Distance[0],
                        xy=fpos, xycoords='data', xytext=(-30, -20),
                        ha='right', va='center', textcoords='offset points',
                        arrowprops=dict(facecolor=color, shrink=0.05),
                        fontsize=16, color=color, annotation_clip=False)
                    lpos = (df.Recall.iloc[-1], df.Precision.iloc[-1])
                    ax1.annotate(
                        df.Distance.iloc[-1],
                        xy=lpos, xycoords='data', xytext=(-30, -20),
                        ha='right', va='center', textcoords='offset points',
                        arrowprops=dict(facecolor=color, shrink=0.05),
                        fontsize=16, color=color, annotation_clip=False)
            else:
                for df, color in cdata:
                    if df.empty:
                        continue
                    ax2.plot(df['Recall'], df['Precision'], color=color, marker='o')
                    fpos = (df.Recall[0], df.Precision[0])
                    ax2.annotate(
                        df.Distance[0],
                        xy=fpos, xycoords='data', xytext=(-30, -20),
                        ha='right', va='center', textcoords='offset points',
                        arrowprops=dict(facecolor=color, shrink=0.05),
                        fontsize=16, color=color, annotation_clip=False)
                    lpos = (df.Recall.iloc[-1], df.Precision.iloc[-1])
                    ax2.annotate(
                        df.Distance.iloc[-1],
                        xy=lpos, xycoords='data', xytext=(-30, -20),
                        ha='right', va='center', textcoords='offset points',
                        arrowprops=dict(facecolor=color, shrink=0.05),
                        fontsize=16, color=color, annotation_clip=False)
        plt.show()

    @staticmethod
    def attacker1_result(result_path: str):
        path = result_path.removesuffix(os.path.sep)
        # Process Acceptance Range Threshold (ART)
        art_low_df, art_high_df = PeformanceResult.get_result_data(
            result_path=f'{path}-art/', fl='art-low-attacker1-result.csv', fh='art-high-attacker1-result.csv',
            lowidx=VEHICULAR_LOW_ATTACK1_HIGH, highidx=VEHICULAR_HIGH_ATTACK1_HIGH, ctype=ChartFeature.ART)

        # Process Sudden Appearance Warning (SAW)
        saw_low_df, saw_high_df = pandas.DataFrame(), pandas.DataFrame()
        # TODO

        # Process Simple Speed Check (SSC)
        ssc_low_df, ssc_high_df = PeformanceResult.get_result_data(
            result_path=f'{path}-ssc/', fl='ssc-low-attacker1-result.csv', fh='ssc-high-attacker1-result.csv',
            lowidx=VEHICULAR_LOW_ATTACK1_HIGH, highidx=VEHICULAR_HIGH_ATTACK1_HIGH, ctype=ChartFeature.SSC)

        # Process Distance Moved Verifier (DMV)
        dmv_low_df, dmv_high_df = PeformanceResult.get_result_data(
            result_path=f'{path}-dmv/', fl='dmv-low-attacker1-result.csv', fh='dmv-high-attacker1-result.csv',
            lowidx=VEHICULAR_LOW_ATTACK1_HIGH, highidx=VEHICULAR_HIGH_ATTACK1_HIGH, ctype=ChartFeature.DMV)

        PeformanceResult.plot(
            data={
                SimulationDensity.LOW: [(art_low_df, 'blue'), (saw_low_df, 'green'),
                                        (ssc_low_df, 'red'), (dmv_low_df, 'cyan')],
                SimulationDensity.HIGH: [(art_high_df, 'blue'), (saw_high_df, 'green'),
                                         (ssc_high_df, 'red'), (dmv_high_df, 'cyan')],
            },
            title1='Attacker Type 1 (30.0% Attackers) - Low Density',
            title2='Attacker Type 1 (30.0% Attackers) - High Density'
        )
