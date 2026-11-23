import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("gate", Path(__file__).resolve().parents[1] / "scripts/eligibility_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def reviewed():
    return {"checked_at": "2026-11-23", "posting": {"state": "open", "source": "official"},
            "checks": [{"dimension": dim, "result": "not_stated", "required": True,
                        "requirement": "full posting reviewed: no condition", "source": "official"}
                       for dim in sorted(gate.DIMENSIONS)]}


def set_check(data, dimension, result="unmet", **kwargs):
    check = next(x for x in data["checks"] if x["dimension"] == dimension)
    check.update(result=result, requirement="explicit condition", candidate_fact="verified fact",
                 candidate_source="candidate record")
    check.update(**kwargs)
    return check


class EligibilityTests(unittest.TestCase):
    def test_graduate_excluded_from_students_only_despite_role_fit(self):
        data = reviewed()
        data["role_score"] = 100
        set_check(data, "education", requirement="students only", candidate_fact="graduate")
        self.assertEqual(gate.assess(data)["route"], "excluded")

    def test_unknown_fulltime_needs_confirmation(self):
        data = reviewed()
        set_check(data, "availability", "unknown")
        self.assertFalse(gate.assess(data)["eligible_for_primary"])
        self.assertEqual(gate.assess(data)["route"], "needs_confirmation")

    def test_missing_reviews_do_not_pass(self):
        data = reviewed()
        data["checks"] = []
        self.assertEqual(gate.assess(data)["route"], "needs_confirmation")

    def test_explicit_experience_exception_is_only_supplemental(self):
        data = reviewed()
        set_check(data, "experience", exception="supplemental", policy_source="profile: allow 1-3yr supplemental")
        self.assertEqual(gate.assess(data)["route"], "supplemental")
        set_check(data, "availability", "unknown")
        self.assertEqual(gate.assess(data)["route"], "needs_confirmation")

    def test_exception_cannot_relax_degree(self):
        data = reviewed()
        set_check(data, "education", exception="supplemental", policy_source="profile")
        with self.assertRaises(ValueError):
            gate.assess(data)

    def test_preference_is_not_blocker(self):
        data = reviewed()
        set_check(data, "location", required=False)
        self.assertTrue(gate.assess(data)["eligible_for_primary"])

    def test_multiple_conditions_in_same_dimension_keep_blocker(self):
        data = reviewed()
        check = set_check(data, "education")
        other = copy.deepcopy(check)
        other["result"] = "met"
        data["checks"].append(other)
        self.assertEqual(gate.assess(data)["route"], "excluded")

    def test_closed_and_unconfirmed_postings_do_not_pass(self):
        for state, route in [("closed", "closed"), ("unknown", "needs_confirmation")]:
            data = reviewed()
            data["posting"]["state"] = state
            self.assertEqual(gate.assess(data)["route"], route)

    def test_claimed_match_requires_candidate_evidence(self):
        data = reviewed()
        check = set_check(data, "education", "met")
        del check["candidate_source"]
        with self.assertRaises(ValueError):
            gate.assess(data)

    def test_invalid_input_rejected(self):
        for field, value in [("result", "eligible"), ("required", "false")]:
            data = reviewed()
            data["checks"][0][field] = value
            with self.assertRaises(ValueError):
                gate.assess(data)

    def test_existing_application_data_not_mutated(self):
        data = reviewed()
        data["application"] = {"status": "submitted", "result": "rejected"}
        before = copy.deepcopy(data)
        result = gate.assess(data)
        self.assertEqual(data, before)
        self.assertEqual(result["record_action"], "preserve_existing_application_history")


if __name__ == "__main__":
    unittest.main()
