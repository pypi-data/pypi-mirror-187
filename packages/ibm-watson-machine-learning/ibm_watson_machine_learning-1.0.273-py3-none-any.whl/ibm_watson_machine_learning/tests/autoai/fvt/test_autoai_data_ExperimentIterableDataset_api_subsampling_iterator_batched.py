#  (C) Copyright IBM Corp. 2021-2023.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

from ibm_watson_machine_learning.data_loaders.datasets.experiment import ExperimentIterableDataset
from ibm_watson_machine_learning.data_loaders.experiment import ExperimentDataLoader

from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes.abstract_autoai_data_subsampling_iterator_batched import \
    AbstractAutoAISubsamplingIteratorBatched
from ibm_watson_machine_learning.tests.utils import is_cp4d


@unittest.skipIf(not is_cp4d(), "Flight Service not supported yet on cloud")
class TestAutoAIRemote(AbstractAutoAISubsamplingIteratorBatched, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """
    def is_non_iterator_available(self):
        return False

    def initialize_data_set_read(self, return_data_as_iterator, enable_sampling, sample_size_limit, sampling_type,
                                             number_of_batch_rows, return_subsampling_stats, experiment_metadata, total_size_limit):
        if not return_data_as_iterator:
            raise Exception(
                'For ExperimentIterableDataset api setting `return_data_as_iterator` to False makes no sense.')

        params = {}

        if sampling_type is not None:
            params['sampling_type'] = sampling_type

        if experiment_metadata is not None:
            params['experiment_metadata'] = experiment_metadata

        if sample_size_limit is not None:
            params['sample_size_limit'] = sample_size_limit

        if number_of_batch_rows is not None:
            params['number_of_batch_rows'] = number_of_batch_rows

        if number_of_batch_rows is not None:
            params['_return_subsampling_stats'] = return_subsampling_stats

        if total_size_limit is not None:
            params['total_size_limit'] = total_size_limit

        dataset = ExperimentIterableDataset(
            connection=self.data_connections[0],
            enable_sampling=enable_sampling,
            **params
        )

        return ExperimentDataLoader(dataset)


if __name__ == '__main__':
    unittest.main()
