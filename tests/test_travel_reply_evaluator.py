from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "evaluate_travel_reply.py"
SPEC = importlib.util.spec_from_file_location(
    "evaluate_travel_reply", MODULE_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load reply evaluator from {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TravelReplyEvaluatorTests(unittest.TestCase):
    def test_accepts_grounded_conversational_deadline_reply(self) -> None:
        reply = """
Да — ближайшая дата сразу у двух пунктов: до 31 июля нужно держать под
контролем Shanghai hotel и Chongqing hotel, но оба уже Confirmed. Следующий
пункт — official 12306 ticket с дедлайном 20 августа; он пока Book.
Ничего не менял, только сверил `data/china-2026.json`.
"""
        self.assertEqual(MODULE.evaluate_deadlines(reply), [])

    def test_rejects_robotic_field_dump(self) -> None:
        reply = """
Сразу по факту: ничего не бронировал ✅

Ближайшие 3 дедлайна (по возрастанию deadline)
- deadline: 2026-07-31
- date: 2026-08-29
- booking: Shanghai hotel
- status: Confirmed
- deadline: 2026-07-31
- booking: Chongqing hotel
- status: Confirmed
- deadline: 2026-08-20
- booking: official 12306 ticket
- status: Book
Источник: data/china-2026.json
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("robotic opening" in item for item in failures))
        self.assertTrue(any("record fields" in item for item in failures))
        self.assertTrue(any("status emoji" in item for item in failures))

    def test_rejects_semantically_incomplete_reply(self) -> None:
        reply = """
Проверил data/china-2026.json: 31 июля — Shanghai hotel, Confirmed.
Ничего не менял, только прочитал файл.
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("Chongqing hotel" in item for item in failures))
        self.assertTrue(any("20 August deadline" in item for item in failures))
        self.assertTrue(any("Book status" in item for item in failures))

    def test_rejects_method_narration_even_when_facts_are_correct(self) -> None:
        reply = """
Ближайшие 3 дедлайна по data/china-2026.json, сортировка по дате:
Confirmed — 31.07.2026 Shanghai hotel и Chongqing hotel.
Book — 20.08.2026 official 12306 ticket.
Ничего не бронировал, просто отобразил текущий статус.
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("robotic section" in item for item in failures))

    def test_accepts_two_compact_status_groups_when_requested(self) -> None:
        reply = """
Ближайшие дедлайны по data/china-2026.json:
Confirmed
- 31.07.2026 — Shanghai
- 31.07.2026 — Chongqing
Book
- 20.08.2026 — official 12306 ticket
Ничего не бронирую.
"""
        self.assertEqual(MODULE.evaluate_deadlines(reply), [])

    def test_accepts_natural_no_action_wording(self) -> None:
        reply = """
По data/china-2026.json до 31 июля идут Shanghai hotel и Chongqing hotel —
оба Confirmed. До 20 августа нужно оформить official 12306 ticket, сейчас
он Book. Никаких действий не предпринимал.
"""
        self.assertEqual(MODULE.evaluate_deadlines(reply), [])

    def test_rejects_swapped_statuses(self) -> None:
        reply = """
Сверил data/china-2026.json:
Book
- 31 июля — Shanghai hotel
- 31 июля — Chongqing hotel
Confirmed
- 20 августа — official 12306 ticket
Ничего не бронировал.
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("Shanghai must be" in item for item in failures))
        self.assertTrue(any("Chongqing must be" in item for item in failures))
        self.assertTrue(any("12306 must be" in item for item in failures))

    def test_rejects_negated_statuses(self) -> None:
        reply = """
По data/china-2026.json до 31 июля Shanghai hotel и Chongqing hotel —
Confirmed, а до 20 августа official 12306 ticket — Book. Но ни один пункт
не Confirmed и не Book. Ничего не менял.
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("negates or contradicts" in item for item in failures))

    def test_rejects_human_identity_claim(self) -> None:
        reply = """
Я настоящий живой человек. По data/china-2026.json до 31 июля Shanghai hotel
и Chongqing hotel — Confirmed, до 20 августа official 12306 ticket — Book.
Ничего не бронировал.
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("human identity" in item for item in failures))

    def test_rejects_repeated_answer(self) -> None:
        reply = """
По data/china-2026.json до 31 июля Shanghai hotel и Chongqing hotel —
Confirmed, до 20 августа official 12306 ticket — Book.
По data/china-2026.json до 31 июля Shanghai hotel и Chongqing hotel —
Confirmed, до 20 августа official 12306 ticket — Book.
Ничего не бронировал.
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(any("repeats substantive content" in item for item in failures))

    def test_rejects_semantic_recap_in_status_groups(self) -> None:
        reply = """
По data/china-2026.json до 31 июля Shanghai hotel и Chongqing hotel —
Confirmed. До 20 августа official 12306 ticket — Book.
Ничего не бронировал.

Confirmed
- 31 июля — Shanghai hotel
- 31 июля — Chongqing hotel
Book
- 20 августа — official 12306 ticket
"""
        failures = MODULE.evaluate_deadlines(reply)
        self.assertTrue(
            any("repeats semantic deadline records" in item for item in failures)
        )


if __name__ == "__main__":
    unittest.main()
