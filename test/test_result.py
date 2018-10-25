
import pytest

inputs = {'Cutoff': [18, 25, 19.5, 22],  # Wind Speed @ Cutoff
          'Max Power': [15, 20, 17, 19],  # Wind Speed @ Max Power
          'Wind Speed': 20}


baseline_cutoff = [True, True, True, False]
baseline_max_power = [True, False, True, True]


@pytest.mark.parametrize('run', [inputs], indirect=True)
class TestClass:

    def test_cutoff(self, run):
        result_cutoff = self.results['Cutoff']
        if result_cutoff != baseline_cutoff:
            assert False, 'Failure in Cutoff test'

    def test_max_power(self, run):
        result_max_power = self.results['Max Power']
        if result_max_power != baseline_max_power:
            assert False, 'Failure in Max Power test'
