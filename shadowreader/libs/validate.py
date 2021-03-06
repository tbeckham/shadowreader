"""
Copyright 2018 Edmunds.com, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
"""

from pytz import timezone, all_timezones

from classes.exceptions import InvalidLambdaEnvVarError
from classes.mytime import MyTime


def validate_test_params(params: dict, tzinfo: timezone):
    """ Validate that test params set in Lambda env var is in proper format """
    if not params:
        return

    required_params = [
        'rate', 'loop_duration', 'replay_start_time', 'base_url'
    ]
    for p in required_params:
        assert p in params, f'Required Lambda env var: {p} not found in test_params: {params}'

    rate = params['rate']
    assert isinstance(rate, float) or isinstance(
        rate, int), f'Rate must be an int or float'
    assert 0 <= rate, f'Test param rate: {rate} must be a float above 0'

    loop_duration = params['loop_duration']
    assert isinstance(loop_duration, int), f'Loop duration must be an int'
    assert 0 < loop_duration, f'Loop duration must be greater than 0'

    replay_start_time = params['replay_start_time']
    replay_start_time = MyTime.set_to_replay_start_time_env_var(
        replay_start_time, tzinfo)
    assert isinstance(replay_start_time, MyTime)


def validate_timezone(tzinfo: str):
    if tzinfo not in all_timezones:
        raise InvalidLambdaEnvVarError(
            f'Timezone not recognized: {tzinfo}. Must be in pytz format')
