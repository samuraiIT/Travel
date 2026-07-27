#!/usr/bin/env python3
"""Deterministic semantic and style gate for simple Travel bot replies."""

from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path


ROBOTIC_OPENINGS = (
    "сразу по факту",
    "итог:",
    "вердикт:",
    "в рамках проекта",
    "ниже представлен",
)
ROBOTIC_SECTIONS = (
    "отдельно по статусу",
    "ближайшие 3 дедлайна (по возрастанию deadline)",
    "сортировка по дате",
    "как iso-дат",
    "просто отобразил текущий статус",
    "last_verified",
)

DATE_31_JULY = ("2026-07-31", "31 июля", "31.07.2026")
DATE_20_AUGUST = ("2026-08-20", "20 августа", "20.08.2026")
SHANGHAI = ("shanghai", "шанха")
CHONGQING = ("chongqing", "чунцин")
TICKET_12306 = ("official 12306 ticket", "12306")

NO_ACTION_PATTERNS = (
    r"\bничего\s+не\s+(?:брониру\w*|брониров\w*|покупа\w*|меня\w*|дела\w*)",
    r"\bникаких\s+(?:внешних\s+)?действий\s+не\s+"
    r"(?:предпринима\w*|выполня\w*|соверша\w*)",
    r"\bне\s+(?:вносил\w*|делал\w*)\s+(?:никаких\s+)?изменений",
    r"\bбез\s+(?:бронирования|покупки|изменений)",
    r"\bтолько\s+(?:проверил\w*|сверил\w*|прочитал\w*|посмотрел\w*)",
)


def contains_any(text: str, variants: tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(variant.casefold() in lowered for variant in variants)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold().replace("ё", "е")).strip()


def _status_heading(line: str) -> str | None:
    cleaned = re.sub(r"^[\s#>*_-]+|[\s#>*_:`—–-]+$", "", line.casefold())
    if cleaned in {"confirmed", "book"}:
        return cleaned
    return None


def _semantic_units(reply: str) -> list[tuple[str, str | None]]:
    """Return sentence/list-item units and an optional status-heading context."""

    units: list[tuple[str, str | None]] = []
    prose_lines: list[str] = []
    active_status: str | None = None

    def flush_prose() -> None:
        if not prose_lines:
            return
        paragraph = _normalize(" ".join(prose_lines))
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
            sentence = sentence.strip()
            if sentence:
                units.append((sentence, None))
        prose_lines.clear()

    for raw_line in reply.splitlines():
        line = raw_line.strip()
        if not line:
            flush_prose()
            continue

        heading = _status_heading(line)
        if heading:
            flush_prose()
            active_status = heading
            continue

        is_list_item = bool(re.match(r"^(?:[-*•]|\d+[.)])\s+", line))
        if is_list_item:
            flush_prose()
            units.append((_normalize(line), active_status))
            continue

        # A plain line inside a status block can still be a compact list item.
        if active_status and contains_any(line, SHANGHAI + CHONGQING + TICKET_12306):
            flush_prose()
            units.append((_normalize(line), active_status))
            continue

        prose_lines.append(line)

    flush_prose()
    return units


def _nearest_distance(text: str, anchor_variants: tuple[str, ...], token: str) -> int:
    anchor_positions = [
        match.start()
        for variant in anchor_variants
        for match in re.finditer(re.escape(variant), text)
    ]
    token_positions = [match.start() for match in re.finditer(rf"\b{token}\b", text)]
    if not anchor_positions or not token_positions:
        return sys.maxsize
    return min(abs(anchor - status) for anchor in anchor_positions for status in token_positions)


def _nearest_variant_distance(
    text: str,
    anchors: tuple[str, ...],
    variants: tuple[str, ...],
) -> int:
    anchor_positions = [
        match.start()
        for variant in anchors
        for match in re.finditer(re.escape(variant), text)
    ]
    variant_positions = [
        match.start()
        for variant in variants
        for match in re.finditer(re.escape(variant), text)
    ]
    if not anchor_positions or not variant_positions:
        return sys.maxsize
    return min(
        abs(anchor - candidate)
        for anchor in anchor_positions
        for candidate in variant_positions
    )


def _assignment_match_count(
    units: list[tuple[str, str | None]],
    item_variants: tuple[str, ...],
    expected_date: tuple[str, ...],
    other_date: tuple[str, ...],
    expected_status: str,
) -> int:
    opposite_status = "book" if expected_status == "confirmed" else "confirmed"
    matches = 0

    for text, heading_status in units:
        if not contains_any(text, item_variants) or not contains_any(text, expected_date):
            continue

        expected_date_distance = _nearest_variant_distance(
            text, item_variants, expected_date
        )
        other_date_distance = _nearest_variant_distance(text, item_variants, other_date)
        if expected_date_distance > 220 or expected_date_distance >= other_date_distance:
            continue

        if heading_status is not None:
            if heading_status == expected_status:
                matches += 1
            continue

        expected_distance = _nearest_distance(text, item_variants, expected_status)
        opposite_distance = _nearest_distance(text, item_variants, opposite_status)
        if expected_distance <= 220 and expected_distance < opposite_distance:
            matches += 1

    return matches


def _repeated_content(reply: str) -> bool:
    normalized_lines = [
        re.sub(r"^[\s#>*•_-]+", "", _normalize(line))
        for line in reply.splitlines()
        if line.strip()
    ]
    substantive_lines = [line for line in normalized_lines if len(line) >= 24]
    if any(count > 1 for count in Counter(substantive_lines).values()):
        return True

    normalized_reply = _normalize(reply)
    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", normalized_reply)
        if len(sentence.strip()) >= 32
    ]
    return any(count > 1 for count in Counter(sentences).values())


def evaluate_deadlines(reply: str) -> list[str]:
    failures: list[str] = []
    stripped = reply.strip()
    lowered = _normalize(stripped)
    lowered_multiline = stripped.casefold().replace("ё", "е")

    required_groups = {
        "31 July deadline": DATE_31_JULY,
        "20 August deadline": DATE_20_AUGUST,
        "Shanghai hotel": SHANGHAI,
        "Chongqing hotel": CHONGQING,
        "12306 ticket": TICKET_12306,
        "Confirmed status": ("confirmed",),
        "Book status": ("book",),
        "source file": ("data/china-2026.json",),
    }
    for label, variants in required_groups.items():
        if not contains_any(stripped, variants):
            failures.append(f"missing {label}")

    if not any(re.search(pattern, lowered) for pattern in NO_ACTION_PATTERNS):
        failures.append("missing explicit no-booking/read-only statement")

    units = _semantic_units(stripped)
    assignments = (
        (
            "Shanghai must be 31 July and Confirmed",
            SHANGHAI,
            DATE_31_JULY,
            DATE_20_AUGUST,
            "confirmed",
        ),
        (
            "Chongqing must be 31 July and Confirmed",
            CHONGQING,
            DATE_31_JULY,
            DATE_20_AUGUST,
            "confirmed",
        ),
        (
            "12306 must be 20 August and Book",
            TICKET_12306,
            DATE_20_AUGUST,
            DATE_31_JULY,
            "book",
        ),
    )
    duplicate_assignments: list[str] = []
    for label, item, expected_date, other_date, expected_status in assignments:
        match_count = _assignment_match_count(
            units, item, expected_date, other_date, expected_status
        )
        if match_count == 0:
            failures.append(f"incorrect or missing association: {label}")
        elif match_count > 1:
            duplicate_assignments.append(label)
    if duplicate_assignments:
        failures.append(
            "reply repeats semantic deadline records: "
            + ", ".join(duplicate_assignments)
        )

    contradiction_patterns = (
        r"\bни\s+один\b.{0,120}\b(?:confirmed|book)\b",
        r"\bне\s+(?:является\s+|имеет\s+статус\s+)?(?:confirmed|book)\b",
        r"\bнет\s+(?:статуса\s+)?(?:confirmed|book)\b",
    )
    if any(re.search(pattern, lowered) for pattern in contradiction_patterns):
        failures.append("reply negates or contradicts the required statuses")

    if len(stripped) > 1400:
        failures.append(f"simple reply is too long: {len(stripped)} characters")

    first_line = lowered_multiline.splitlines()[0].strip() if lowered else ""
    if first_line.startswith(ROBOTIC_OPENINGS):
        failures.append(f"robotic opening: {first_line!r}")

    for section in ROBOTIC_SECTIONS:
        if section in lowered:
            failures.append(f"robotic section: {section!r}")

    field_dump_lines = sum(
        1
        for line in lowered_multiline.splitlines()
        if re.match(r"\s*[•*-]?\s*(deadline|date|booking|status)\s*:", line)
    )
    if field_dump_lines >= 4:
        failures.append("reply dumps record fields instead of speaking naturally")

    markdown_headings = sum(
        1 for line in stripped.splitlines() if line.lstrip().startswith("#")
    )
    if markdown_headings > 1:
        failures.append("simple reply uses too many headings")

    bullet_lines = sum(
        1
        for line in stripped.splitlines()
        if re.match(r"\s*(?:[-*•]|\d+[.)])\s+", line)
    )
    if bullet_lines > 6:
        failures.append("simple reply uses too many list items")

    human_claim_patterns = (
        r"\bя\s+(?:(?:настоящ|жив|реальн)\w*\s+)*человек\b",
        r"\bя\s+не\s+(?:бот|ии|ai)\b",
        r"\bне\s+являюсь\s+(?:ботом|ии|ai)\b",
        r"\bкак\s+(?:(?:настоящ|жив|реальн)\w*\s+)*человек\b",
    )
    if any(re.search(pattern, lowered) for pattern in human_claim_patterns):
        failures.append("reply claims or implies human identity")

    if _repeated_content(stripped):
        failures.append("reply repeats substantive content")

    if stripped.count("✅") > 0:
        failures.append("reply uses automatic status emoji")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "reply_file",
        nargs="?",
        type=Path,
        help="UTF-8 reply file; stdin is used when omitted",
    )
    args = parser.parse_args()

    if args.reply_file:
        reply = args.reply_file.read_text(encoding="utf-8")
    else:
        reply = sys.stdin.read()

    failures = evaluate_deadlines(reply)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("PASS: deadline reply is grounded, concise, and conversational")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
