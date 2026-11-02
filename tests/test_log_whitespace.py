import pytest
from app.analyzer import matches_keyword

@pytest.mark.parametrize('message,keyword', [
    ('out  of memory', 'out of memory'), ('connection\trefused', 'connection refused'),
    ('no space\nleft', 'no space left'), ('internal\u00a0server error', 'internal server error'),
])
def test_log_whitespace_does_not_hide_failure_phrases(message, keyword):
    assert matches_keyword(message, keyword)

def test_phrase_still_requires_separate_words():
    assert not matches_keyword('connectionrefused', 'connection refused')
