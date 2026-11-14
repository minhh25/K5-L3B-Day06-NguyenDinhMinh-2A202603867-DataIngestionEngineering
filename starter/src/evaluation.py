
import re
import unicodedata
from collections import defaultdict
from typing import Any


def normalize_evidence(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def evaluate_query(
    question: dict[str, Any],
    hits: list[dict[str, Any]]
) -> dict[str, Any]:
    required = [
        "id",
        "split",
        "question"
    ]

    missing = [key for key in required if key not in question]

    if missing:
        raise ValueError(f"Missing question fields: {missing}")

    gold_sets = question.get("gold_evidence")

    if gold_sets is None:
        for field in ("gold_source_id", "gold_page", "evidence_quote"):
            if field not in question:
                raise ValueError(f"Missing question field: {field}")
        gold_sets = [{
            "gold_source_id": question["gold_source_id"],
            "gold_page": question["gold_page"],
            "evidence_quote": question["evidence_quote"]
        }]

    if not isinstance(gold_sets, list) or not gold_sets:
        raise ValueError("gold_evidence must be a non-empty list")

    def as_list(value):
        return value if isinstance(value, list) else [value]

    for gold in gold_sets:
        if not isinstance(gold, dict):
            raise ValueError("Each gold_evidence alternative must be an object")
        for field in ("gold_source_id", "gold_page", "evidence_quote"):
            if field not in gold or not as_list(gold[field]):
                raise ValueError(f"Invalid gold field: {field}")
        if not all(isinstance(s, str) and s.strip() for s in as_list(gold["gold_source_id"])):
            raise ValueError("Gold sources must be nonempty strings")
        if not all(type(p) is int and p > 0 for p in as_list(gold["gold_page"])):
            raise ValueError("Gold pages must be positive integers")
        if not all(isinstance(q, str) and normalize_evidence(q) for q in as_list(gold["evidence_quote"])):
            raise ValueError("Gold quotes must be nonempty strings")

    def match_gold(hit, gold):
        sources = as_list(gold["gold_source_id"])
        pages = as_list(gold["gold_page"])
        quotes = as_list(gold["evidence_quote"])

        hit_source = hit.get("document_id")
        hit_page = hit.get("page")
        metadata = hit.get("metadata") or {}

        page_start = metadata.get("page_start", hit_page)
        page_end = metadata.get("page_end", hit_page)

        source_ok = hit_source in sources

        page_ok = all(
            isinstance(page, int)
            and isinstance(page_start, int)
            and isinstance(page_end, int)
            and page_start <= page <= page_end
            for page in pages
        )

        content = normalize_evidence(hit.get("text", ""))

        evidence_ok = all(
            isinstance(quote, str)
            and bool(normalize_evidence(quote))
            and normalize_evidence(quote) in content
            for quote in quotes
        )

        return source_ok and page_ok and evidence_ok

    evaluated_hits = []

    for rank, hit in enumerate(hits[:3], start=1):
        matched = any(match_gold(hit, gold) for gold in gold_sets)

        evaluated_hits.append({
            "rank": rank,
            "chunk_id": hit.get("chunk_id"),
            "document_id": hit.get("document_id"),
            "source": hit.get("source"),
            "page": hit.get("page"),
            "text": hit.get("text", ""),
            "score": hit.get("score"),
            "metadata": hit.get("metadata", {}),
            "evidence_match": matched
        })

    first_match_rank = next(
        (
            hit["rank"]
            for hit in evaluated_hits
            if hit["evidence_match"]
        ),
        None
    )

    return {
        "id": question["id"],
        "split": question["split"],
        "strategy": question.get("strategy", "unknown"),
        "question": question["question"],
        "expected_answer": question.get("expected_answer"),
        "gold_evidence": gold_sets,
        "filter": question.get("filter"),
        "hits": evaluated_hits,
        "hit_at_1": int(first_match_rank == 1),
        "evidence_hit_at_3": int(first_match_rank is not None),
        "first_match_rank": first_match_rank
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    groups = defaultdict(list)

    for trace in traces:
        strategy = trace.get("strategy", "unknown")
        split = trace.get("split", "unknown")
        groups[(strategy, split)].append(trace)

    summary = {}

    for (strategy, split), items in sorted(groups.items()):
        total = len(items)

        hit_1 = sum(
            int(item["hit_at_1"])
            for item in items
        )

        hit_3 = sum(
            int(item["evidence_hit_at_3"])
            for item in items
        )

        if strategy not in summary:
            summary[strategy] = {}

        summary[strategy][split] = {
            "total_questions": total,
            "hit_at_1_count": hit_1,
            "hit_at_1": hit_1 / total,
            "evidence_hit_at_3_count": hit_3,
            "evidence_hit_at_3": hit_3 / total
        }

    return summary
