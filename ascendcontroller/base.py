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
import errno
import time
import pandas
from enum import Enum
import multiprocessing as mp
from typing_extensions import Self
from abc import ABC, abstractmethod
from multiprocessing import cpu_count
from typing import Iterable, NamedTuple, Sequence


class ResultType(Enum):
    Normal = 1,
    Attack = 2


class ConfusionMatrix(Enum):
    TP = 1,
    FP = 2,
    TN = 3,
    FN = 4


class FeatureResult(NamedTuple):
    data: pandas.DataFrame
    error: RuntimeError = None
    prefix: str = ''
    suffix: str = ''


class FeatureParam(ABC):
    # Data Frame to process
    data: pandas.DataFrame

    @staticmethod
    def build(data: pandas.DataFrame) -> Self:
        raise NotImplementedError


class Feature(ABC):
    """ Feature Base class

        Extend this class to implement new algorithms.
        The 'process' method should return required value and an optional filename.
    """

    def __init__(self, factory: FeatureParam):
        self.factory = factory

    @abstractmethod
    def process(self, data: pandas.DataFrame) -> FeatureResult:
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


class CsvRunner:
    def __init__(
        self, path: str, destination: str, features: Iterable[Feature],
        processes: int = 0, prefix: str = 'result', ext: str = 'csv',
        idxfilter: Sequence = []
    ):
        # Root path for files
        self.path = path
        # Change Dataset directory
        os.chdir(self.path)
        # Result Destination Path
        self.destination = destination
        # Create target directory
        self.create_destination()
        # List of algorithms to process
        self.features = features
        # CPU Count
        self.processes = cpu_count() if processes <= 0 else processes
        # Result file prefix
        self.prefix = prefix
        # Result file extension
        self.ext = ext
        # File filter indexes
        self.idxfilter = idxfilter

    def process(self):
        # Finished file list
        finished = [int(re.search(r'\d+', f).group()) for f in os.listdir(self.destination)
                    if os.path.isfile(f'{self.destination}{f}')]
        finished.sort()
        # List files in current directory
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        files.sort()
        # Filter unprocessed files
        files = list(filter(lambda f: int(re.search(r'\d+', f).group()) not in finished, files))
        # Filter index files
        files = list(filter(lambda f: int(re.search(r'\d+', f).group()) in self.idxfilter, files))
        # Create files Data Frame
        simulations = pandas.Series(dtype=pandas.StringDtype(), data=files).reset_index(drop=True)
        if simulations.count() > 0:
            start_time = time.time()
            print('Running features...')
            print("Start time: " + time.strftime("%H:%M:%S.{}".format(str(start_time %
                  1)[2:])[:15], time.localtime(start_time)))
            # Process files within workers
            with mp.Pool(processes=self.processes) as pool:
                pool.map(self.worker, enumerate(simulations))
            elapsed = time.time() - start_time
            print("Elapsed time: " + time.strftime("%H:%M:%S.{}".format(str(elapsed %
                  1)[2:])[:15], time.gmtime(elapsed)))

    # noinspection PyMethodMayBeStatic
    def worker(self, sim):
        try:
            idsim, file = sim
            # print(f'Processing file {file} on Thread "{mp.current_process().name}"...')
            data_frame = pandas.read_csv(file)
            # Run all features for each simulation file.
            for feature in self.features:
                result: FeatureResult = feature.process(data_frame)
                # Check for current feature output error
                if result.error is not None:
                    print(f'Error processing {file} on feature {feature}. Error: {result.error}')
                    continue
                else:
                    # If the main data is not empty, save the CSV file.
                    if not result.data.empty:
                        idx = int(re.search(r'\d+', file).group())
                        output_file = f'{self.destination}{result.prefix}{self.prefix}{idx:03d}{result.suffix}.{self.ext}'
                        result.data.to_csv(output_file)
        except Exception as e:
            print(e)

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
