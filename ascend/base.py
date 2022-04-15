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

import os
import re
import errno
from enum import Enum
import multiprocessing as mp
from typing_extensions import Self
from abc import ABC, abstractmethod
from multiprocessing import cpu_count
from typing import Any, Generic, Iterable, NamedTuple

import pandas


class ResultType(Enum):
    Normal = 1,
    Attack = 2


class ConfusionMatrix(Enum):
    TP = 1,
    FP = 2,
    TN = 3,
    FN = 4


class FeatureResult(NamedTuple):
    data: Any
    error: RuntimeError


class FeatureParam(ABC):
    @staticmethod
    def build(data) -> Self:
        raise NotImplementedError


class Feature(ABC):
    """ Feature Base class

        Extend this class to implement new algorithms.
        The 'process' method should return required value and an optional filename.
    """

    def __init__(self, factory: FeatureParam):
        self.factory = factory

    @abstractmethod
    def process(self, data) -> FeatureResult:
        pass

    # noinspection PyMethodMayBeStatic
    def confusion_matrix(self, real: bool, dectected: bool):
        if real is True and dectected is True:
            return ConfusionMatrix.TP
        elif real is False and dectected is False:
            return ConfusionMatrix.TN
        elif real is True and dectected is False:
            return ConfusionMatrix.FN
        elif real is False and dectected is True:
            return ConfusionMatrix.FP


class FeatureRunner:
    def __init__(
            self, path: str, destination: str, algorithms: Iterable[Feature],
            processes: int = 0, prefix: str = 'result', ext: str = 'csv'):
        # Root path for files
        self.path = path
        # Change Dataset directory
        os.chdir(self.path)
        # Result Destination Path
        self.destination = destination
        # Create target directory
        self.create_destination()
        # List of algorithms to process
        self.algorithms = algorithms
        # CPU Count
        self.processes = cpu_count() if processes <= 0 else processes
        # Result file prefix
        self.prefix = prefix
        # Result file extension
        self.ext = ext

    def process(self):
        # Finished file list
        finished = [re.search(r'\d+', f).group() for f in os.listdir(self.destination)
                    if os.path.isfile(f'{self.destination}{f}')]
        finished.sort()
        # List files in current directory
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        # Filter unprocessed files
        files = list(filter(lambda f: re.search(r'\d+', f).group() not in finished, files))
        simulations = pandas.Series(files).sort_values().reset_index(drop=True)
        # Process files within workers
        with mp.Pool(processes=self.processes) as pool:
            pool.map(self.worker, enumerate(simulations))

    # noinspection PyMethodMayBeStatic
    def worker(self, sim):
        idsim, file = sim
        print(f'Processing file {file} on Thread "{mp.current_process().name}"...')
        output_file = f'{self.destination}{self.prefix}{idsim:03d}.{self.ext}'
        data_frame = pandas.read_csv(file)
        data_log = pandas.DataFrame()
        for index, row in data_frame.iterrows():
            row_data = pandas.DataFrame()
            # Runs all algorithms for each line of the simulation file.
            for alg in self.algorithms:
                result: FeatureResult = alg.process(row)
                # If result file is not None, save the result DataFrame in the new algorithm file. Otherwise,
                # merge the result DataFrame into the main file.
                if result.error is not None:
                    print(f'Error processing {file} on feature {alg}. Error: {result.error}')
                    continue
                else:
                    row_data = pandas.concat([row_data, result.data], axis=1)
            data_log = pandas.concat([data_log, row_data])
        # If the main data is not empty, save the CSV file.
        if not data_log.empty:
            data_log.to_csv(output_file)

    def create_destination(self):
        dest = self.destination
        if dest:
            directory = os.path.dirname(dest)
            if len(directory) > 0:
                if not os.path.exists(directory):
                    try:
                        os.makedirs(os.path.dirname(dest))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
