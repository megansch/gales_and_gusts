import pytest


def compare_wind_speed(inputs):
    results = []
    for cutoff in inputs['Cutoff']:
        if inputs['Wind Speed'] > cutoff:
            results.append(True)
        else:
            results.append(False)

    return results


def compare_max_power(inputs):
    results = []
    for max_p in inputs['Max Power']:
        if inputs['Wind Speed'] > max_p:
            results.append(True)
        else:
            results.append(False)

    return results


@pytest.fixture(scope='class')
def run(request):

    results = {}
    inputs = request.param

    results['Cutoff'] = compare_wind_speed(inputs)
    results['Max Power'] = compare_max_power(inputs)

    yield results
