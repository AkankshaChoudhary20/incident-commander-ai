from app.analyzer import analyze
from app.models import Signal

def test_gateway_failure_status_codes_match_application_failure():
    for code in ['502', '504']:
        causes, actions = analyze([Signal(incident_id='test', type='log', source='gateway', severity='critical', timestamp='2026-11-07T00:00:00Z', message=f'HTTP {code} from upstream')])
        assert causes[0].cause == 'Application or upstream service failure'
        assert actions[0].priority != 'low'

def test_gateway_status_codes_do_not_match_larger_numbers():
    causes, _ = analyze([Signal(incident_id='test', type='log', source='gateway', severity='critical', timestamp='2026-11-07T00:00:00Z', message='request_id=15024 elapsed=15040')])
    assert causes[0].cause == 'Insufficient evidence for a specific root cause'
