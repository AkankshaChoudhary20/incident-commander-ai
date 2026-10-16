from datetime import datetime, timezone
import pytest
from app.models import Signal
from app.analyzer import analyze

def signal(message):
    return Signal(incident_id='test',source='log',type='log',message=message,timestamp=datetime.now(timezone.utc))

@pytest.mark.parametrize('message',['Room service is healthy','Processed 5000 requests successfully','Processed 50321 messages'])
def test_short_keywords_do_not_match_inside_unrelated_words(message):
    causes,_=analyze([signal(message)])
    assert causes[0].cause=='Insufficient evidence for a specific root cause'

@pytest.mark.parametrize('message',['Container OOMKilled','Kernel invoked OOM-killer','HTTP 503: service unavailable','HTTP 500 error'])
def test_real_failure_tokens_still_match(message):
    causes,_=analyze([signal(message)])
    assert causes[0].cause!='Insufficient evidence for a specific root cause'

def test_evidence_contains_only_signals_that_actually_match():
    causes,_=analyze([signal('Room service healthy'),signal('OOM-killer terminated process')])
    memory=next(c for c in causes if c.cause=='Memory exhaustion')
    assert memory.evidence==['OOM-killer terminated process']

def test_failure_phrases_do_not_span_unrelated_signals():
    causes,_=analyze([signal('connection'),signal('refused')])
    assert causes[0].cause=='Insufficient evidence for a specific root cause'
