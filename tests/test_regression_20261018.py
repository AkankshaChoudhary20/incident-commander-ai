import unittest
from datetime import datetime, timezone
from app.analyzer import analyze
from app.models import Signal

class RemediationOrderTests(unittest.TestCase):
    def test_remediations_follow_ranked_causes(self):
        signal = Signal(incident_id='INC-1', source='test', type='log', message='timeout; oom out of memory memory limit', timestamp=datetime.now(timezone.utc), severity='critical', service='api')
        causes, advice = analyze([signal])
        self.assertEqual(causes[0].cause, 'Memory exhaustion')
        self.assertIn('memory', advice[0].action.lower())
        self.assertIn('dependency health', advice[1].action)

    def test_fallback_keeps_matching_advice(self):
        causes, advice = analyze([])
        self.assertEqual(len(causes), 1)
        self.assertEqual(advice[0].priority, 'low')
