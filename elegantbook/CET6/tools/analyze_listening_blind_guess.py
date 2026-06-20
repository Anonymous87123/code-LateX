from __future__ import annotations

import csv
import argparse
import difflib
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cet 6" / "_listening_analysis_output"
TEXT_PARSE = OUT / "texts" / "parse"
OCR_PARSE = OUT / "ocr_pages" / "parse"
RAW_PARSE = OUT / "raw_parse_texts"
PDF_DIR = ROOT / "cet 6" / (
    "Some PDF files do not have a text layer, and in such cases, "
    "OCR (Optical Character Recognition) will fail"
)


AUDITED_ANSWER_OVERRIDES: dict[tuple[str, str], dict[str, str]] = {
    ("2022.06.set1", "9"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: OCR page says AI was first used to find a powerful new antibiotic molecule; option A matches.",
    },
    ("2022.12.set1", "9"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says short stress doubled the growth of new brain cells in rats; option B matches.",
    },
    ("2022.12.set1", "13"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says minor issues can transform into a major problem or crisis; option D matches.",
    },
    ("2022.12.set1", "21"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says customers leave comments on social media praising the products; option B matches.",
    },
    ("2022.12.set1", "23"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says coins from New York public-park fountains go toward maintenance; option C matches.",
    },
    ("2022.12.set1", "25"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says Thomas Morgan fished out thousands of dollars using a magnetic stick; option D matches.",
    },
    ("2023.03.set1", "6"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says managers use persuasive/manipulative language; option C masks irrational choices.",
    },
    ("2023.03.set1", "13"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says the wedding was now-canceled/called off; option B says it was cancelled.",
    },
    ("2023.06.set1", "3"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says the man also missed his roommates and felt lonely after moving out; option C matches.",
    },
    ("2023.06.set1", "14"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says the federal government commissioned private wagons to carry the mail; option B matches.",
    },
    ("2023.06.set1", "21"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says marketers should pay attention to latest technological developments; option B matches.",
    },
    ("2023.06.set1", "23"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says the initial study analyzed friends' impact on self-esteem and well-being; option A matches.",
    },
    ("2023.06.set2", "10"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says risk-free activities deprive kids of testing themselves and overcoming fears; option C matches.",
    },
    ("2023.06.set2", "19"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says Nebraska City was a treeless plain in 1854; option C matches.",
    },
    ("2024.12.set1", "8"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says the woman's grades were a mixed bag and not consistent; option C matches.",
    },
    ("2024.12.set1", "9"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says street-sign photos provide evidence to the computer that the user is human; option D matches.",
    },
    ("2024.12.set1", "21"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says the brain makes predictions using color; option B matches.",
    },
    ("2024.12.set2", "14"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says aspirational goals should include goals to help other people; option C matches.",
    },
    ("2024.12.set2", "23"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says scents travel directly to emotional and memory centers of the brain; option D matches.",
    },
    ("2022.06.set1", "12"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: explanation says most people detect lying by observing people they know and then generalizing; option C, observation, matches the direct answer.",
    },
    ("2022.09.set1", "7"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: explanation says on signing the contract the man must pay the first month's rent and a deposit; option B matches.",
    },
    ("2022.09.set1", "8"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker/explanation says his wife will be excited because the wardrobes can hold all those shoes; option D matches.",
    },
    ("2022.09.set1", "10"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says parents should seek input from children about purchases; option C matches.",
    },
    ("2022.09.set1", "14"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: explanation says a normal person can actively compete with people who perform better; option B matches.",
    },
    ("2022.09.set1", "18"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: explanation says late adolescents prioritize romantic relationships over same-sex friendships; option A matches.",
    },
    ("2022.09.set1", "21"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says if the disability does not affect job performance, applicants can choose whether/when to share it; option C matches.",
    },
    ("2022.09.set1", "24"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: explanation says essay writing is best with all background noise minimized; option A, keep everything quiet, matches.",
    },
    ("2022.09.set1", "25"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: explanation says shy, quiet people were most negatively affected by distractions; option B matches.",
    },
    ("2022.12.set1", "11"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: explanation says chronic stress makes people more prone to illness; option C matches.",
    },
    ("2022.12.set2", "11"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: explanation says forgiving the offender requires reflecting on why the offense occurred and developing empathy; option C matches.",
    },
    ("2022.12.set2", "20"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says prejudices are dangerous because they keep us from learning the truth; option D matches.",
    },
    ("2022.12.set2", "24"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: explanation says the Vietnam experience made the speaker more mature than his friends; option A matches.",
    },
    ("2023.03.set1", "4"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says both parents are in their 70s but have no health problems and hardly get sick; option A matches.",
    },
    ("2023.06.set1", "11"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says insight occurs during reflection and relaxation after intense activity; option D matches.",
    },
    ("2023.06.set2", "7"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says this is his first job after university and he has little prior working experience; option D matches.",
    },
    ("2023.06.set2", "11"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says if adventure sports are too much, introduce other outdoor adventures; option B matches.",
    },
    ("2023.06.set2", "20"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says Morton founded the state's first newspaper and wrote editorials promoting tree planting; option D matches.",
    },
    ("2023.12.set1", "10"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says Atkinson's books touch on themes of love and loss; option A matches.",
    },
    ("2023.12.set1", "16"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: recording opens by asking what makes humans different from other species; option A matches.",
    },
    ("2024.06.set1", "7"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says people will see only a blur without a telescope; option A matches.",
    },
    ("2024.06.set2", "12"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: explanation says the speaker slept/dozed through the entire rough ferry ride; option B matches.",
    },
    ("2024.06.set2", "16"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says people underestimate how much they can be swayed by a convincing article; option D matches.",
    },
    ("2024.06.set2", "21"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says more women are mothers of adult children who celebrate the holiday; option C matches.",
    },
    ("2024.06.set2", "23"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says NASA tests were in sealed containers unlike homes/offices; option B matches.",
    },
    ("2024.06.set2", "25"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says scientific research should continually re-examine and question findings; option D matches.",
    },
    ("2024.12.set1", "7"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says internal medicine covers much and ties many specialties together; option B matches.",
    },
    ("2024.12.set2", "21"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says about half of the global population can be considered middle class; option B matches.",
    },
    ("2025.06.set1", "9"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says researchers proposed an explanation for older people's memory-retrieval difficulty; option C matches.",
    },
    ("2025.06.set1", "12"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says workers are often not in control of how they work and related outcomes; option C matches.",
    },
    ("2025.06.set2", "4"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says John will cast the deciding vote if there is a tie; option D matches.",
    },
    ("2025.06.set2", "9"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says stray dogs followed pointing gestures without prior training; option D matches.",
    },
    ("2025.12.set1", "1"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker introduces Lord Blackwell as an experienced and distinguished career diplomat; option A matches.",
    },
    ("2025.12.set1", "8"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says the whole managerial hierarchy wants early implementation of the project; option C matches.",
    },
    ("2025.12.set1", "17"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says the baggage tag may be torn off on the conveyor belt; option A matches.",
    },
    ("2025.12.set2", "4"): {
        "answer": "D",
        "confidence": "high",
        "evidence": "manual_audit: marker says the canteen had a massive renovation; option D matches.",
    },
    ("2025.12.set2", "10"): {
        "answer": "C",
        "confidence": "high",
        "evidence": "manual_audit: marker says the study compared frequent and rare vegetarian-food eaters; option C matches.",
    },
    ("2025.12.set2", "11"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: explanation says altered menu designs made frequent vegetarian-food eaters less likely to choose vegetarian dishes; option A matches.",
    },
    ("2025.12.set2", "13"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says existing indoor-air purification technologies can be inefficient, expensive, or harmful; option A matches.",
    },
    ("2025.12.set2", "14"): {
        "answer": "B",
        "confidence": "high",
        "evidence": "manual_audit: marker says people spend even more time indoors when outdoor air quality is poor; option B matches.",
    },
    ("2025.12.set2", "23"): {
        "answer": "A",
        "confidence": "high",
        "evidence": "manual_audit: marker says every decision has made us the person we are today; option A matches.",
    },
}


def closure_override(answer: str, note: str = "verified by full closure pass") -> dict[str, str]:
    return {
        "answer": answer,
        "confidence": "high",
        "evidence": f"full_closure_audit: {note}; see listening_full_closure_audit.csv for transcript/explanation snippets.",
    }


FULL_CLOSURE_ANSWER_OVERRIDES: dict[tuple[str, str], dict[str, str]] = {
    # 2022.06 set 1: rows where earlier majority-vote extraction was polluted by adjacent columns.
    ("2022.06.set1", "7"): closure_override("C"),
    ("2022.06.set1", "8"): closure_override("D"),
    ("2022.06.set1", "10"): closure_override("B"),
    ("2022.06.set1", "11"): closure_override("B"),
    ("2022.06.set1", "13"): closure_override("D"),
    ("2022.06.set1", "22"): closure_override("A"),

    # 2022.09 set 1: source text uses spaced question numbers such as "2 .";
    # the original option extractor skipped these before the closure pass.
    ("2022.09.set1", "1"): closure_override("C", "raw parse text answer heading"),
    ("2022.09.set1", "2"): closure_override("D", "raw parse text answer heading"),
    ("2022.09.set1", "3"): closure_override("A", "raw parse text answer heading"),
    ("2022.09.set1", "4"): closure_override("B", "raw parse text answer heading"),
    ("2022.09.set1", "5"): closure_override("C", "raw parse text answer heading"),
    ("2022.09.set1", "6"): closure_override("B", "raw parse text answer heading"),
    ("2022.09.set1", "7"): closure_override("B", "raw parse text answer heading"),
    ("2022.09.set1", "8"): closure_override("D", "raw parse text answer heading"),
    ("2022.09.set1", "9"): closure_override("D", "raw parse text answer heading"),
    ("2022.09.set1", "10"): closure_override("C", "raw parse text answer heading"),
    ("2022.09.set1", "11"): closure_override("A", "raw parse text answer heading"),
    ("2022.09.set1", "12"): closure_override("D", "raw parse text answer heading"),
    ("2022.09.set1", "13"): closure_override("C", "raw parse text answer heading"),
    ("2022.09.set1", "14"): closure_override("B", "raw parse text answer heading"),
    ("2022.09.set1", "15"): closure_override("A", "raw parse text answer heading"),
    ("2022.09.set1", "16"): closure_override("D", "raw parse text answer heading"),
    ("2022.09.set1", "17"): closure_override("A", "raw parse text answer heading"),
    ("2022.09.set1", "18"): closure_override("A", "raw parse text answer heading"),
    ("2022.09.set1", "19"): closure_override("B", "raw parse text answer heading"),
    ("2022.09.set1", "20"): closure_override("C", "raw parse text answer heading"),
    ("2022.09.set1", "21"): closure_override("D", "raw parse text answer heading"),
    ("2022.09.set1", "22"): closure_override("B", "raw parse text answer heading"),
    ("2022.09.set1", "23"): closure_override("C", "raw parse text answer heading"),
    ("2022.09.set1", "24"): closure_override("A", "raw parse text answer heading"),
    ("2022.09.set1", "25"): closure_override("B", "raw parse text answer heading"),

    ("2022.12.set2", "10"): closure_override("B"),
    ("2022.12.set2", "13"): closure_override("C"),
    ("2022.12.set2", "25"): closure_override("C"),

    ("2023.03.set1", "7"): closure_override("B"),
    ("2023.03.set1", "10"): closure_override("C"),
    ("2023.03.set1", "21"): closure_override("C"),

    ("2023.06.set1", "1"): closure_override("B"),
    ("2023.06.set1", "19"): closure_override("A"),
    ("2023.06.set2", "1"): closure_override("D"),
    ("2023.06.set2", "8"): closure_override("B"),
    ("2023.06.set2", "18"): closure_override("A"),
    ("2023.06.set2", "21"): closure_override("B"),

    ("2023.12.set1", "2"): closure_override("C"),
    ("2023.12.set1", "3"): closure_override("A"),
    ("2023.12.set1", "4"): closure_override("D"),
    ("2023.12.set1", "5"): closure_override("A"),
    ("2023.12.set1", "6"): closure_override("C"),
    ("2023.12.set1", "7"): closure_override("D"),
    ("2023.12.set1", "8"): closure_override("B"),
    ("2023.12.set1", "9"): closure_override("D"),
    ("2023.12.set1", "14"): closure_override("D"),
    ("2023.12.set1", "17"): closure_override("D"),
    ("2023.12.set1", "25"): closure_override("B"),
    ("2023.12.set2", "1"): closure_override("D"),
    ("2023.12.set2", "3"): closure_override("D"),
    ("2023.12.set2", "9"): closure_override("B"),
    ("2023.12.set2", "13"): closure_override("C"),
    ("2023.12.set2", "18"): closure_override("D"),
    ("2023.12.set2", "19"): closure_override("B"),
    ("2023.12.set2", "21"): closure_override("D"),
    ("2023.12.set2", "23"): closure_override("B"),
    ("2023.12.set2", "25"): closure_override("D"),

    ("2024.06.set1", "1"): closure_override("B"),
    ("2024.06.set1", "2"): closure_override("A"),
    ("2024.06.set1", "3"): closure_override("C"),
    ("2024.06.set1", "4"): closure_override("C"),
    ("2024.06.set1", "5"): closure_override("A"),
    ("2024.06.set1", "6"): closure_override("B"),
    ("2024.06.set1", "8"): closure_override("D"),
    ("2024.06.set1", "11"): closure_override("B"),
    ("2024.06.set1", "18"): closure_override("B"),
    ("2024.06.set1", "24"): closure_override("D"),
    ("2024.06.set2", "1"): closure_override("A"),
    ("2024.06.set2", "15"): closure_override("C"),
    ("2024.06.set2", "17"): closure_override("A"),
    ("2024.06.set2", "19"): closure_override("C"),
    ("2024.06.set2", "22"): closure_override("B"),
    ("2024.06.set2", "24"): closure_override("A"),
    ("2024.12.set1", "11"): closure_override("D"),
    ("2024.12.set1", "20"): closure_override("D"),
    ("2024.12.set2", "11"): closure_override("B"),
    ("2024.12.set2", "20"): closure_override("C"),

    ("2025.06.set1", "2"): closure_override("B"),
    ("2025.06.set1", "3"): closure_override("D"),
    ("2025.06.set1", "4"): closure_override("A"),
    ("2025.06.set1", "10"): closure_override("B"),
    ("2025.06.set1", "16"): closure_override("D"),
    ("2025.06.set1", "17"): closure_override("A"),
    ("2025.06.set1", "19"): closure_override("A"),
    ("2025.06.set1", "21"): closure_override("C"),
    ("2025.06.set1", "25"): closure_override("B"),

    ("2025.06.set2", "1"): closure_override("D"),
    ("2025.06.set2", "2"): closure_override("B"),
    ("2025.06.set2", "3"): closure_override("A"),
    ("2025.06.set2", "5"): closure_override("B"),
    ("2025.06.set2", "6"): closure_override("C"),
    ("2025.06.set2", "7"): closure_override("A"),
    ("2025.06.set2", "8"): closure_override("B"),
    ("2025.06.set2", "10"): closure_override("C"),
    ("2025.06.set2", "11"): closure_override("B"),
    ("2025.06.set2", "12"): closure_override("A"),
    ("2025.06.set2", "13"): closure_override("C"),
    ("2025.06.set2", "14"): closure_override("A"),
    ("2025.06.set2", "15"): closure_override("D"),
    ("2025.06.set2", "17"): closure_override("A"),
    ("2025.06.set2", "18"): closure_override("D"),
    ("2025.06.set2", "19"): closure_override("A"),
    ("2025.06.set2", "20"): closure_override("D"),
    ("2025.06.set2", "21"): closure_override("B"),
    ("2025.06.set2", "22"): closure_override("C"),
    ("2025.06.set2", "23"): closure_override("D"),
    ("2025.06.set2", "24"): closure_override("B"),
    ("2025.06.set2", "25"): closure_override("C"),

    ("2025.12.set1", "2"): closure_override("D"),
    ("2025.12.set1", "3"): closure_override("C"),
    ("2025.12.set1", "4"): closure_override("A"),
    ("2025.12.set1", "5"): closure_override("B"),
    ("2025.12.set1", "6"): closure_override("B"),
    ("2025.12.set1", "7"): closure_override("D"),
    ("2025.12.set1", "9"): closure_override("D"),
    ("2025.12.set1", "10"): closure_override("A"),
    ("2025.12.set1", "11"): closure_override("C"),
    ("2025.12.set1", "12"): closure_override("A"),
    ("2025.12.set1", "13"): closure_override("B"),
    ("2025.12.set1", "14"): closure_override("B"),
    ("2025.12.set1", "15"): closure_override("D"),
    ("2025.12.set1", "16"): closure_override("B"),
    ("2025.12.set1", "18"): closure_override("D"),
    ("2025.12.set1", "19"): closure_override("C"),
    ("2025.12.set1", "20"): closure_override("B"),
    ("2025.12.set1", "21"): closure_override("D"),
    ("2025.12.set1", "22"): closure_override("C"),
    ("2025.12.set1", "23"): closure_override("A"),
    ("2025.12.set1", "24"): closure_override("C"),
    ("2025.12.set1", "25"): closure_override("D"),

    ("2025.12.set2", "1"): closure_override("B"),
    ("2025.12.set2", "2"): closure_override("A"),
    ("2025.12.set2", "3"): closure_override("C"),
    ("2025.12.set2", "5"): closure_override("A"),
    ("2025.12.set2", "6"): closure_override("B"),
    ("2025.12.set2", "7"): closure_override("D"),
    ("2025.12.set2", "8"): closure_override("C"),
    ("2025.12.set2", "9"): closure_override("B"),
    ("2025.12.set2", "12"): closure_override("C"),
    ("2025.12.set2", "15"): closure_override("D"),
    ("2025.12.set2", "16"): closure_override("C"),
    ("2025.12.set2", "17"): closure_override("B"),
    ("2025.12.set2", "18"): closure_override("D"),
    ("2025.12.set2", "19"): closure_override("D"),
    ("2025.12.set2", "20"): closure_override("A"),
    ("2025.12.set2", "21"): closure_override("C"),
    ("2025.12.set2", "22"): closure_override("C"),
    ("2025.12.set2", "24"): closure_override("D"),
    ("2025.12.set2", "25"): closure_override("B"),
}


AUDITED_ANSWER_OVERRIDES.update(FULL_CLOSURE_ANSWER_OVERRIDES)


MANUAL_AUDIT_ROWS: list[dict[str, str]] = [
    {
        "key": "2022.06.set1",
        "question": "9",
        "old_answer": "C",
        "evidence_summary": "AI first used to find a powerful new antibiotic molecule",
    },
    {
        "key": "2022.12.set1",
        "question": "9",
        "old_answer": "C",
        "evidence_summary": "stress doubled the growth of new brain cells in rats",
    },
    {
        "key": "2022.12.set1",
        "question": "13",
        "old_answer": "C",
        "evidence_summary": "minor issues can transform into major problem or crisis",
    },
    {
        "key": "2022.12.set1",
        "question": "21",
        "old_answer": "C",
        "evidence_summary": "customers leave comments on social media praising products",
    },
    {
        "key": "2022.12.set1",
        "question": "23",
        "old_answer": "A",
        "evidence_summary": "NYC fountain coins go toward fountain maintenance",
    },
    {
        "key": "2022.12.set1",
        "question": "25",
        "old_answer": "A",
        "evidence_summary": "Thomas Morgan used a magnetic stick to steal change",
    },
    {
        "key": "2023.03.set1",
        "question": "6",
        "old_answer": "B",
        "evidence_summary": "managers use manipulative language to mask irrational choices",
    },
    {
        "key": "2023.03.set1",
        "question": "13",
        "old_answer": "A",
        "evidence_summary": "the wedding was cancelled/called off",
    },
    {
        "key": "2023.06.set1",
        "question": "3",
        "old_answer": "A",
        "evidence_summary": "the man had a similar feeling after moving out",
    },
    {
        "key": "2023.06.set1",
        "question": "14",
        "old_answer": "D",
        "evidence_summary": "federal government commissioned private wagons",
    },
    {
        "key": "2023.06.set1",
        "question": "21",
        "old_answer": "A",
        "evidence_summary": "marketers should follow latest technological developments",
    },
    {
        "key": "2023.06.set1",
        "question": "23",
        "old_answer": "C",
        "evidence_summary": "initial study analyzed friends impact on self-esteem and well-being",
    },
    {
        "key": "2023.06.set2",
        "question": "10",
        "old_answer": "D",
        "evidence_summary": "risk-free activities deprive kids of testing themselves/overcoming fears",
    },
    {
        "key": "2023.06.set2",
        "question": "19",
        "old_answer": "A",
        "evidence_summary": "Nebraska City was a treeless plain",
    },
    {
        "key": "2024.12.set1",
        "question": "8",
        "old_answer": "D",
        "evidence_summary": "grades were a mixed bag/not consistent",
    },
    {
        "key": "2024.12.set1",
        "question": "9",
        "old_answer": "B",
        "evidence_summary": "street-sign photos prove the user is human to the computer",
    },
    {
        "key": "2024.12.set1",
        "question": "21",
        "old_answer": "D",
        "evidence_summary": "the brain makes predictions using color",
    },
    {
        "key": "2024.12.set2",
        "question": "14",
        "old_answer": "B",
        "evidence_summary": "aspirational goals should include helping other people",
    },
    {
        "key": "2024.12.set2",
        "question": "23",
        "old_answer": "C",
        "evidence_summary": "scents travel directly to emotional and memory centers",
    },
]


def apply_audited_answer_overrides(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row.get("key", ""), row.get("question", ""))
        seen.add(key)
        override = AUDITED_ANSWER_OVERRIDES.get(key)
        if not override:
            continue
        row["answer"] = override["answer"]
        row["confidence"] = override["confidence"]
        row["votes"] = json.dumps({override["answer"]: 1}, ensure_ascii=False)
        row["sources"] = (row.get("sources", "") + "; manual_audit").strip("; ")
        row["evidence"] = override["evidence"]
    for (key, question), override in AUDITED_ANSWER_OVERRIDES.items():
        if (key, question) in seen:
            continue
        rows.append(
            {
                "key": key,
                "question": question,
                "section": "A" if int(question) <= 8 else "B" if int(question) <= 15 else "C",
                "answer": override["answer"],
                "confidence": override["confidence"],
                "votes": json.dumps({override["answer"]: 1}, ensure_ascii=False),
                "sources": "manual_audit",
                "evidence": override["evidence"],
            }
        )
    return sorted(rows, key=question_sort_key)


def safe_stem(path: Path) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", path.stem).strip("_")


CHINESE_SET_NUMBERS = {"一": 1, "二": 2, "三": 3}


def parse_key_from_name(name: str) -> str:
    year = month = set_no = None
    m = re.search(r"(20\d{2})[.年](\d{1,2})", name)
    if m:
        year, month = int(m.group(1)), int(m.group(2))
    m = re.search(r"第\s*([123])\s*套", name)
    if m:
        set_no = int(m.group(1))
    if set_no is None:
        for han, num in CHINESE_SET_NUMBERS.items():
            if f"第{han}套" in name or f"{han}套" in name:
                set_no = num
                break
    return f"{year or 0:04d}.{month or 0:02d}.set{set_no or 0}"


def load_ocr():
    from rapidocr_onnxruntime import RapidOCR

    return RapidOCR()


def page_text_by_columns(image: Path, ocr) -> str:
    result, _elapsed = ocr(str(image))
    if not result:
        return ""

    rows = []
    for box, text, score in result:
        xs = [float(point[0]) for point in box]
        ys = [float(point[1]) for point in box]
        rows.append(
            {
                "x": min(xs),
                "x2": max(xs),
                "y": min(ys),
                "text": str(text),
                "score": float(score),
            }
        )
    if not rows:
        return ""

    max_x = max(row["x2"] for row in rows)
    mid = max_x / 2
    answer_y = min(
        (row["y"] for row in rows if "\u7b54\u6848" in row["text"]),
        default=None,
    )
    if answer_y is not None:
        rows = [row for row in rows if row["y"] > answer_y + 10]

    left: list[dict] = []
    right: list[dict] = []
    full: list[dict] = []
    for row in rows:
        # Full-width transcript lines are not explanation text. Keep them last,
        # so answer blocks are mostly parsed column by column.
        if row["x"] < mid * 0.65 and row["x2"] > mid * 1.25:
            full.append(row)
        elif row["x"] < mid:
            left.append(row)
        else:
            right.append(row)

    def join(part: list[dict]) -> str:
        return "\n".join(row["text"] for row in sorted(part, key=lambda r: (r["y"], r["x"])))

    return "\n".join(chunk for chunk in [join(left), join(right), join(full)] if chunk)


Q_HEAD = re.compile(
    r"(?m)(^|\n)\s*(\d{1,2})[.．]\s*(?:What|Why|How|When|Where|Who|Which|Whatis|Whatdo|Whatdoes|Whatdid)",
    re.IGNORECASE,
)

ANSWER_PATTERNS = [
    re.compile(r"(?:因此|故|所以|由此可知|这表明|可知)?\s*\u7b54\u6848\s*(?:为|是)?\s*([ABCD])\s*[)）]?", re.I),
    re.compile(r"([ABCD])\s*[)）]\s*【\u7cbe\u6790】"),
]


def extract_answers_from_text(text: str, key: str, source: str) -> list[dict[str, str]]:
    matches = list(Q_HEAD.finditer(text))
    rows = []
    for i, match in enumerate(matches):
        question = int(match.group(2))
        if not 1 <= question <= 25:
            continue
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        answers: list[str] = []
        for pattern in ANSWER_PATTERNS:
            answers.extend(pattern.findall(block))
        answers = [a.upper() for a in answers if a and a.upper() in "ABCD"]
        if not answers:
            continue
        # In a column-clean block, the explicit conclusion is usually the last
        # answer-like token; the leading "A)【精析】" agrees in clean cases.
        answer = answers[-1]
        confidence = "high" if len(set(answers)) == 1 else "medium"
        rows.append(
            {
                "key": key,
                "question": str(question),
                "section": "A" if question <= 8 else "B" if question <= 15 else "C",
                "answer": answer,
                "confidence": confidence,
                "source": source,
                "answers_seen": "".join(answers),
                "evidence": re.sub(r"\s+", " ", block[:400]).strip(),
            }
        )
    return rows


QUESTION_HEAD_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])([0-9IlOo]{1,2})[.\uff0e\u3002](?=\s*[A-Za-z])"),
    re.compile(r"(?<![A-Za-z0-9])([0-9IlOo]{1,2})[.\uff0e\u3002]\s*[ABCD][)\uff09]"),
]

ANSWER_CUE_WORDS = (
    r"\u7531\u6b64\u53ef\u77e5|\u56e0\u6b64|\u6240\u4ee5|\u6545|"
    r"\u53ef\u89c1|\u8868\u660e|\u8fd9\u8868\u660e|\u53ef\u5f97\u51fa|\u53ef\u77e5"
)
ANSWER_POSITIVE_WORDS = (
    r"\u6b63\u786e\u7b54\u6848|\u6b63\u786e\u9009\u9879|\u6b63\u786e|"
    r"\u76f8\u7b26|\u540c\u4e49\u8f6c\u8ff0|\u603b\u7ed3\u6982\u62ec|"
    r"\u76f4\u63a5\u590d\u73b0|\u539f\u8bcd\u590d\u73b0|\u5b8c\u5168\u4e00\u81f4"
)
ANSWER_CUE_PATTERNS = [
    re.compile(r"\u7b54\u6848\s*(?:\u4e3a|\u662f|\u9009\u9879|\u9009)?\s*([ABCD])", re.I),
    re.compile(r"\u6b63\u786e\u7b54\u6848\s*(?:\u4e3a|\u662f)?\s*([ABCD])", re.I),
    re.compile(rf"(?:{ANSWER_CUE_WORDS})[^\u3002\uff1b;]{{0,60}}?\u9009\u9879\s*([ABCD])", re.I),
    re.compile(rf"(?:{ANSWER_CUE_WORDS})[^\u3002\uff1b;]{{0,60}}?([ABCD])\u9879", re.I),
    re.compile(rf"(?:\u9009\u9879\s*)?([ABCD])(?:\u9879)?[^\u3002\uff1b;]{{0,80}}?(?:{ANSWER_POSITIVE_WORDS})", re.I),
    re.compile(r"(?:\u6545|\u56e0\u6b64|\u6240\u4ee5)\s*\u9009(?:\u9879)?\s*([ABCD])", re.I),
    re.compile(r"([ABCD])\s*[)\uff09]\s*(?:\u3010)?\u7cbe\u6790", re.I),
]
ANSWER_NEGATIVE_CONTEXT_RE = re.compile(
    r"\u6392\u9664|\u5e72\u6270|\u672a\u63d0\u53ca|\u4e0d\u662f|\u5e76\u975e|"
    r"\u76f8\u6096|\u9519\u8bef|\u65e0\u4e2d\u751f\u6709|\u4e0d\u7b26|\u4e0d\u4e00\u81f4"
)
ANSWER_POSITIVE_CONTEXT_RE = re.compile(ANSWER_POSITIVE_WORDS + r"|\u7b54\u6848")
ANSWER_PAGE_HINT_RE = re.compile(
    r"\u7b54\u6848|\u7cbe\u6790|\u7531\u6b64\u53ef\u77e5|\u6b63\u786e|\u9009\u9879"
)
ANSWER_HEADING_RE = re.compile(
    r"(?<![A-Za-z0-9])([ABCD8])\s*[)\uff09]\s*(?:[\u3010\[])?\s*\u7cbe\s*\u6790",
    re.I,
)


def normalize_answer_letter(answer: str) -> str:
    answer = answer.upper()
    return "B" if answer == "8" else answer


def normalize_question_token(token: str) -> int | None:
    normalized = (
        token.replace("I", "1")
        .replace("l", "1")
        .replace("O", "0")
        .replace("o", "0")
    )
    return int(normalized) if normalized.isdigit() else None


def question_heads(text: str) -> list[tuple[int, int]]:
    heads: set[tuple[int, int]] = set()
    for pattern in QUESTION_HEAD_PATTERNS:
        for match in pattern.finditer(text):
            question = normalize_question_token(match.group(1))
            if question is not None and 1 <= question <= 25:
                heads.add((match.start(), question))
    return sorted(heads, key=lambda item: item[0])


def answer_cues(block: str) -> list[tuple[int, str]]:
    cues: list[tuple[int, str]] = []
    for pattern in ANSWER_CUE_PATTERNS:
        for match in pattern.finditer(block):
            context = block[match.start() : min(len(block), match.end() + 80)]
            if ANSWER_NEGATIVE_CONTEXT_RE.search(context) and not ANSWER_POSITIVE_CONTEXT_RE.search(context):
                continue
            cues.append((match.start(), match.group(1).upper()))
    return sorted(cues, key=lambda item: item[0])


def extract_answers_from_text(
    text: str, key: str, source: str, source_kind: str = "parse"
) -> list[dict[str, str]]:
    matches = question_heads(text)
    rows = []
    for i, (start, question) in enumerate(matches):
        if not 1 <= question <= 25:
            continue
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        block = text[start:end]
        heading_answers = [
            normalize_answer_letter(match.group(1)) for match in ANSWER_HEADING_RE.finditer(block)
        ]
        if heading_answers:
            answers = heading_answers
            method = "answer_heading"
            answer = answers[0]
        else:
            answers = [answer for _pos, answer in answer_cues(block)]
            method = "answer_phrase"
            answer = answers[-1] if answers else ""
        if not answers:
            continue
        confidence = "high" if len(set(answers)) == 1 else "medium"
        rows.append(
            {
                "key": key,
                "question": str(question),
                "section": "A" if question <= 8 else "B" if question <= 15 else "C",
                "answer": answer,
                "confidence": confidence,
                "source": source,
                "source_kind": source_kind,
                "method": method,
                "answers_seen": "".join(answers),
                "evidence": re.sub(r"\s+", " ", block[:400]).strip(),
            }
        )
    return rows


def is_parse_pdf_name(path: Path) -> bool:
    if path.suffix.lower() != ".pdf":
        return False
    return any(token in path.name for token in ("\u89e3\u6790", "\u8be6\u89e3", "\u7b54\u6848"))


def raw_parse_stem(stem: str) -> str:
    return stem[:-4] if stem.endswith(".raw") else stem


def normalize_parse_stem(stem: str) -> str:
    return re.sub(r"\.ocr(?:_p\d+-\d+_r\d+)?$", "", stem)


def ensure_raw_parse_text_cache() -> None:
    RAW_PARSE.mkdir(exist_ok=True)
    if not PDF_DIR.exists():
        return
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        if not is_parse_pdf_name(pdf):
            continue
        cache_path = RAW_PARSE / f"{safe_stem(pdf)}.raw.txt"
        if cache_path.exists():
            continue
        proc = subprocess.run(
            ["pdftotext", "-raw", "-enc", "UTF-8", str(pdf), str(cache_path)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            cache_path.write_text("", encoding="utf-8")


def ensure_rebuilt_answer_page_cache(*, cached_only: bool) -> None:
    cache = OUT / "rebuilt_answer_pages"
    cache.mkdir(exist_ok=True)
    ocr = None

    for text_file in sorted(TEXT_PARSE.glob("*.ocr_p*.txt")):
        stem = normalize_parse_stem(text_file.stem)
        text = text_file.read_text(encoding="utf-8", errors="replace")
        pages = text.split("\n\f\n")
        image_dir = OCR_PARSE / stem
        if not image_dir.exists():
            continue

        for idx, page in enumerate(pages, start=1):
            if idx > 8 and "25." not in page and "(25)" not in page and "[25]" not in page:
                # Listening answer explanations usually finish early; keep a
                # small exception for late Section C pages.
                continue
            if "\u7b54\u6848" not in page and "【\u7cbe\u6790】" not in page:
                continue
            image = image_dir / f"page-{idx:02d}.png"
            if not image.exists():
                continue
            page_cache = cache / f"{stem}.page-{idx:02d}.columns.txt"
            if page_cache.exists():
                column_text = page_cache.read_text(encoding="utf-8", errors="replace")
            elif cached_only:
                continue
            else:
                if ocr is None:
                    ocr = load_ocr()
                column_text = page_text_by_columns(image, ocr)
                page_cache.write_text(column_text, encoding="utf-8")


def load_option_rows() -> list[dict[str, str]]:
    with (OUT / "question_option_records.csv").open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def collect_answer_candidates(*, cached_only: bool = False) -> list[dict[str, str]]:
    ensure_raw_parse_text_cache()
    ensure_rebuilt_answer_page_cache(cached_only=cached_only)

    answer_rows: list[dict[str, str]] = []

    for page_cache in sorted((OUT / "rebuilt_answer_pages").glob("*.columns.txt")):
        stem = page_cache.name.split(".page-")[0]
        key = parse_key_from_name(stem)
        text = page_cache.read_text(encoding="utf-8", errors="replace")
        answer_rows.extend(
            extract_answers_from_text(text, key, page_cache.name, source_kind="columns")
        )

    for raw_file in sorted(RAW_PARSE.glob("*.raw.txt")):
        stem = raw_parse_stem(raw_file.stem)
        key = parse_key_from_name(stem)
        text = raw_file.read_text(encoding="utf-8", errors="replace")
        answer_rows.extend(extract_answers_from_text(text, key, raw_file.name, source_kind="raw"))

    for text_file in sorted(TEXT_PARSE.glob("*.txt")):
        stem = normalize_parse_stem(text_file.stem)
        key = parse_key_from_name(stem)
        text = text_file.read_text(encoding="utf-8", errors="replace")
        answer_rows.extend(extract_answers_from_text(text, key, text_file.name, source_kind="parse"))

    existing_path = OUT / "listening_answer_key_rebuilt.csv"
    if existing_path.exists():
        try:
            with existing_path.open(encoding="utf-8-sig", newline="") as f:
                existing_rows = list(csv.DictReader(f))
        except Exception:
            existing_rows = []
        for row in existing_rows:
            if row.get("answer") in {"A", "B", "C", "D"}:
                copied = dict(row)
                copied["source"] = row.get("sources", "previous_answer_key")
                copied["source_kind"] = "previous"
                copied["method"] = "previous_answer_key"
                copied["answers_seen"] = row.get("answer", "")
                answer_rows.append(copied)

    return answer_rows


def choose_answer_candidate(rows: list[dict[str, str]]) -> dict[str, str] | None:
    for source_kind in ("columns", "raw", "parse", "previous"):
        source_rows = [row for row in rows if row.get("source_kind") == source_kind]
        if not source_rows:
            continue
        high_rows = [row for row in source_rows if row.get("confidence") == "high"] or source_rows
        heading_rows = [row for row in high_rows if row.get("method") == "answer_heading"] or high_rows
        counts = Counter(row["answer"] for row in heading_rows if row.get("answer") in {"A", "B", "C", "D"})
        if not counts:
            continue
        answer, _count = counts.most_common(1)[0]
        return next(row for row in heading_rows if row.get("answer") == answer)
    return None


def rebuild_answer_key(*, cached_only: bool = False) -> list[dict[str, str]]:
    option_rows = load_option_rows()
    targets = {(row["key"], row["question"]) for row in option_rows}
    candidates = collect_answer_candidates(cached_only=cached_only)

    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        key = (row.get("key", ""), row.get("question", ""))
        if key in targets:
            grouped[key].append(row)

    final: list[dict[str, str]] = []
    for option_row in sorted(option_rows, key=question_sort_key):
        key = (option_row["key"], option_row["question"])
        override = AUDITED_ANSWER_OVERRIDES.get(key)
        selected = choose_answer_candidate(grouped.get(key, []))

        if override:
            answer = override["answer"]
            confidence = override.get("confidence", "high")
            votes = json.dumps({answer: 1}, ensure_ascii=False)
            sources = "full_closure_audit"
            evidence = override.get("evidence", "")
        elif selected:
            answer = selected["answer"]
            confidence = "high"
            same_source_counts = Counter(
                row["answer"]
                for row in grouped[key]
                if row.get("source_kind") == selected.get("source_kind") and row.get("answer") in {"A", "B", "C", "D"}
            )
            votes = json.dumps(same_source_counts, ensure_ascii=False)
            sources = selected.get("source", "")
            evidence = selected.get("evidence", "")
        else:
            answer = ""
            confidence = "missing"
            votes = "{}"
            sources = ""
            evidence = ""

        final.append(
            {
                "key": option_row["key"],
                "question": option_row["question"],
                "section": option_row["section"],
                "answer": answer,
                "confidence": confidence,
                "votes": votes,
                "sources": sources,
                "evidence": evidence,
            }
        )

    return sorted(final, key=question_sort_key)


OPTION_LABEL_RE = re.compile(r"(?<!\w)([ABCD])\s*[)）]\s*")
BOILERPLATE_PATTERNS = [
    re.compile(r"\bQuestions\s+\d+\s+to\s+\d+\b.*$", re.I),
    re.compile(r"\bSection\s+[ABC]\b.*$", re.I),
    re.compile(r"\bDirections:? .*$", re.I),
    re.compile(r"\bPart\s*(?:[\]\[]+|[A-Z0-9]{1,4}).*$"),
    re.compile(r"\s*第\s*\d+\s*页\s*", re.I),
    re.compile(r"\s*20\s*\d{2}.*?页.*?(?=\b[ABCD]\s*[)）]|$)", re.I),
    re.compile(r"\s*20\s*\d{2}.*?b\s*y\s*:\s*.*?(?=\b[ABCD]\s*[)）]|$)", re.I),
    re.compile(r"\s*b\s*y\s*:\s*.*?(?=\b[ABCD]\s*[)）]|$)", re.I),
]


def normalize_option_text(raw: str) -> str:
    text = raw.replace("）", ")").replace("（", "(")
    text = re.sub(r"\s+", " ", text).strip()
    match = re.match(r"\s*\d+\.\s*(.*)", text)
    text = match.group(1) if match else text
    changed = True
    while changed:
        changed = False
        for pattern in BOILERPLATE_PATTERNS:
            new_text = pattern.sub(" ", text)
            if new_text != text:
                text = new_text
                changed = True
    return re.sub(r"\s+", " ", text).strip(" ;.・•■,，")


def split_options(raw: str) -> dict[str, str]:
    text = normalize_option_text(raw)
    labels = list(OPTION_LABEL_RE.finditer(text))
    options: dict[str, str] = {}
    for i, label in enumerate(labels):
        letter = label.group(1)
        start = label.end()
        end = labels[i + 1].start() if i + 1 < len(labels) else len(text)
        value = normalize_option_text(text[start:end])
        if value and letter not in options:
            options[letter] = value
    return options


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]{1,}", text.lower())


CONTENT_STOPWORDS = {
    "a",
    "an",
    "the",
    "to",
    "of",
    "in",
    "on",
    "for",
    "from",
    "by",
    "with",
    "about",
    "into",
    "over",
    "under",
    "and",
    "or",
    "but",
    "as",
    "at",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "it",
    "its",
    "they",
    "their",
    "them",
    "he",
    "she",
    "his",
    "her",
    "this",
    "that",
    "these",
    "those",
    "do",
    "does",
    "did",
    "doing",
    "have",
    "has",
    "had",
    "having",
    "can",
    "could",
    "will",
    "would",
    "should",
    "may",
    "might",
    "must",
    "not",
    "no",
    "more",
    "most",
    "less",
    "least",
    "very",
    "so",
    "such",
    "only",
    "own",
    "same",
    "other",
    "another",
    "each",
    "all",
    "any",
    "some",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "who",
    "what",
    "why",
    "how",
    "when",
    "where",
    "which",
    "than",
    "then",
}


def content_words(text: str) -> list[str]:
    result: list[str] = []
    for word in words(text):
        if word in CONTENT_STOPWORDS:
            continue
        if len(word) > 4 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 4 and word.endswith("ing"):
            word = word[:-3]
        elif len(word) > 3 and word.endswith("ed"):
            word = word[:-2]
        elif len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        result.append(word)
    return result


def char_grams(text: str, n: int = 3) -> set[str]:
    clean = re.sub(r"[^a-z]+", " ", text.lower()).strip()
    clean = re.sub(r"\s+", " ", clean)
    if not clean:
        return set()
    if len(clean) < n:
        return {clean}
    return {clean[i : i + n] for i in range(len(clean) - n + 1)}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    return len(left & right) / len(left | right)


def option_similarity_score(left: str, right: str) -> float:
    left_words = set(content_words(left))
    right_words = set(content_words(right))
    token_jaccard = jaccard(left_words, right_words)
    token_dice = (
        2 * len(left_words & right_words) / (len(left_words) + len(right_words))
        if left_words and right_words
        else 0.0
    )
    char_jaccard = jaccard(char_grams(left), char_grams(right))
    sequence_ratio = difflib.SequenceMatcher(
        None,
        re.sub(r"\s+", " ", left.lower()),
        re.sub(r"\s+", " ", right.lower()),
    ).ratio()
    return 0.45 * token_jaccard + 0.25 * token_dice + 0.20 * char_jaccard + 0.10 * sequence_ratio


def compact_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.I) is not None


ANSWER_EVIDENCE_FLAG_PATTERNS = [
    ("question_range", re.compile(r"Questions\s+\d+\s+to\s+\d+", re.I)),
    (
        "section_or_part",
        re.compile(r"\bSection\s+[ABC]\b|\bPart\s+(?:II|III|IV)\b|Reading Comprehension", re.I),
    ),
]

ANSWER_EVIDENCE_CONTAMINATION_RE = re.compile(
    r"Questions\s+\d+\s+to\s+\d+|\bSection\s+[ABC]\b|\bPart\s+(?:II|III|IV)\b|Reading Comprehension",
    re.I,
)


def answer_evidence_flags(text: str) -> list[str]:
    return [name for name, pattern in ANSWER_EVIDENCE_FLAG_PATTERNS if pattern.search(text)]


def is_evaluable_answer_row(row: dict[str, str]) -> bool:
    return row.get("confidence") in {"high", "audited_high"} and row.get("answer") in {
        "A",
        "B",
        "C",
        "D",
    }


def question_sort_key(row: dict[str, str]) -> tuple[str, int]:
    try:
        question = int(row.get("question", "0"))
    except ValueError:
        question = 0
    return row.get("key", ""), question


def build_answer_audit_rows(answer_key: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in sorted(answer_key, key=question_sort_key):
        flags = answer_evidence_flags(row.get("evidence", ""))
        if not flags:
            continue
        rows.append(
            {
                "key": row.get("key", ""),
                "question": row.get("question", ""),
                "answer": row.get("answer", ""),
                "confidence": row.get("confidence", ""),
                "flags": "/".join(flags),
            }
        )
    return rows


def build_manual_answer_audit_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    listed: set[tuple[str, str]] = set()
    for row in sorted(MANUAL_AUDIT_ROWS, key=question_sort_key):
        listed.add((row["key"], row["question"]))
        override = AUDITED_ANSWER_OVERRIDES[(row["key"], row["question"])]
        rows.append(
            {
                "key": row["key"],
                "question": row["question"],
                "old_answer": row["old_answer"],
                "audited_answer": override["answer"],
                "evidence_summary": row["evidence_summary"],
            }
        )
    for key, question in sorted(AUDITED_ANSWER_OVERRIDES, key=lambda item: (item[0], int(item[1]))):
        if (key, question) in listed:
            continue
        override = AUDITED_ANSWER_OVERRIDES[(key, question)]
        rows.append(
            {
                "key": key,
                "question": question,
                "old_answer": "",
                "audited_answer": override["answer"],
                "evidence_summary": override["evidence"].replace("manual_audit: ", ""),
            }
        )
    return rows


def inferred_unit_for_question(question: str) -> str:
    q = int(question)
    ranges = [
        (1, 4, "Conversation Questions 1-4"),
        (5, 8, "Conversation Questions 5-8"),
        (9, 11, "Passage Questions 9-11"),
        (12, 15, "Passage Questions 12-15"),
        (16, 18, "Recording Questions 16-18"),
        (19, 21, "Recording Questions 19-21"),
        (22, 25, "Recording Questions 22-25"),
    ]
    for start, end, label in ranges:
        if start <= q <= end:
            return label
    return ""


def is_generic_closure_evidence(text: str) -> bool:
    return text.startswith("full_closure_audit:")


def choose_fallback_marker_source(
    answer_row: dict[str, str], explanation_row: dict[str, str]
) -> tuple[str, str]:
    answer_evidence = answer_row.get("evidence", "")
    explanation_evidence = explanation_row.get("evidence", "")
    snippet = (
        answer_evidence
        if answer_evidence and not is_generic_closure_evidence(answer_evidence)
        else explanation_evidence or answer_evidence
    )
    answer_source = answer_row.get("sources", "")
    source = (
        answer_source
        if answer_source and answer_source != "full_closure_audit"
        else explanation_row.get("parse_file", "") or answer_source
    )
    return source, snippet


def build_full_closure_audit_rows(answer_key: list[dict[str, str]]) -> list[dict[str, str]]:
    option_rows = load_option_rows()
    answer_map = {(row["key"], row["question"]): row for row in answer_key}

    marker_map: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    marker_path = OUT / "answer_marker_records.csv"
    if marker_path.exists():
        with marker_path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                marker_map[(row["key"], row["question"])].append(row)

    explanation_map: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    explanation_path = OUT / "answer_explanation_records.csv"
    if explanation_path.exists():
        with explanation_path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                explanation_map[(row["key"], row["question"])].append(row)

    rows: list[dict[str, str]] = []
    for option_row in sorted(option_rows, key=question_sort_key):
        key = (option_row["key"], option_row["question"])
        answer_row = answer_map.get(key, {})
        options = split_options(option_row["raw_options"])
        markers = marker_map.get(key, [])
        marker = markers[0] if markers else {}
        explanations = explanation_map.get(key, [])
        matched_explanation = next(
            (row for row in explanations if row.get("answer") == answer_row.get("answer")),
            {},
        )
        matching_explanation = matched_explanation or (explanations[0] if explanations else {})
        fallback_marker_used = False
        if not markers:
            fallback_source, fallback_snippet = choose_fallback_marker_source(
                answer_row, matched_explanation or matching_explanation
            )
            if fallback_snippet and fallback_source:
                marker = {
                    "parse_file": fallback_source,
                    "unit": inferred_unit_for_question(option_row["question"]),
                    "snippet": fallback_snippet,
                }
                fallback_marker_used = True

        notes: list[str] = []
        if len(options) != 4:
            notes.append("option_split_check")
        if not answer_row.get("answer"):
            notes.append("missing_answer")
        if fallback_marker_used:
            notes.append("fallback_transcript_marker")
        elif not markers:
            notes.append("missing_transcript_marker")
        if len(markers) > 1:
            notes.append(f"multiple_markers={len(markers)}")
        if not answer_row.get("evidence") and not matching_explanation:
            notes.append("missing_explanation_snippet")

        non_blocking_notes = {"fallback_transcript_marker"}
        if len(markers) > 1:
            non_blocking_notes.add(f"multiple_markers={len(markers)}")
        status = "closed" if all(note in non_blocking_notes for note in notes) else "review"
        rows.append(
            {
                "key": option_row["key"],
                "question": option_row["question"],
                "section": option_row["section"],
                "option_A": options.get("A", ""),
                "option_B": options.get("B", ""),
                "option_C": options.get("C", ""),
                "option_D": options.get("D", ""),
                "answer": answer_row.get("answer", ""),
                "answer_source": answer_row.get("sources", ""),
                "answer_confidence": answer_row.get("confidence", ""),
                "transcript_parse_file": marker.get("parse_file", ""),
                "transcript_unit": marker.get("unit", ""),
                "transcript_snippet": marker.get("snippet", ""),
                "explanation_source": matching_explanation.get("parse_file", answer_row.get("sources", "")),
                "explanation_snippet": answer_row.get("evidence", "")
                or matching_explanation.get("evidence", ""),
                "status": status,
                "notes": "; ".join(notes),
            }
        )
    return rows


FEATURES = {
    "absolute": r"\b(all|always|never|only|completely|entirely|none|every|must)\b",
    "negation": r"\b(no|not|never|cannot|can't|without|lack|avoid|prevent|refrain|resist|unable|impossible|inefficient|unwilling|unaware|unhappy|unhealthy)\b",
    "comparison": r"\b(more|less|higher|lower|better|worse|fewer|larger|smaller|increase|decrease|reduce|reduced|double|doubled|twice|than|above|below|decline|growth)\b",
    "advice_plan": r"\b(should|need|needs|plan|plans|intend|intends|advise|advice|suggest|recommend|try to|make sure|bring|take|leave|prepare|always)\b",
    "research": r"\b(research|researchers|experiment|scientist|scientists|survey|data|finding|findings)\b|\bstudies\b|\bstudy found\b|\bstudy showed\b",
    "future": r"\b(future|will|would|plan|plans|intend|intends|hope|going to|next|add|expand|open)\b",
    "example": r"\b(Boston|rats?|mice|hospital|doctor|millionaires?|apps?|bears?|students?|children|parents|workers)\b",
    "cause": r"\b(because|reason|cause|causes|caused|lead|leads|result|results|due to|owing to|stem|stems)\b",
    "moderate": r"\b(may|might|can|could|tend|tends|likely|some|often|usually|mostly|partly|slightly|tiny|small)\b",
    "extreme_bad": r"\b(all|always|never|only|completely|entirely|none|every|must|impossible|cannot|can't)\b",
}


SIGNAL_SCAN_PATTERNS = {
    "absolute": FEATURES["absolute"],
    "negation": FEATURES["negation"],
    "comparison": FEATURES["comparison"],
    "advice_plan": FEATURES["advice_plan"],
    "research": r"\b(research|researchers|experiment|scientist|scientists|survey|data|finding|findings|methodology|journal)\b|\bstudies\b|\bstudy found\b|\bstudy showed\b",
    "future": r"\b(future|will|would|plan|plans|intend|intends|hope|going to|next|add|expand|open|expect|expects|expected|improve)\b",
    "example_broad": FEATURES["example"],
    "cause": FEATURES["cause"],
    "number": r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|hundreds?|thousands?|millions?|billion|percent|percentage|times)\b",
    "abstract_core": r"\b(issue|problem|purpose|impact|effect|risk|benefit|relationship|correlation|attitude|confidence|productivity|satisfaction|anxiety|welfare|strategy|value|role|quality|ability|concept|mechanism|meaning|characteristic|focus|importance|worth)\b",
    "evaluation": r"\b(successful|curious|positive|negative|anxiety|worth|valuable|important|appealing|effective|ineffective|beneficial|harmful|healthy|unhealthy|satisfied|satisfaction|confidence|confident)\b",
    "generic_abstract": r"\b(impact|effect|ability|value|role|quality|importance|significance)\b",
    "problem_risk": r"\b(problem|problems|challenge|challenges|concern|concerns|risk|risks|crisis|threat|issue|issues)\b",
}


def option_features(option: str) -> set[str]:
    return {name for name, pattern in FEATURES.items() if has(pattern, option)}


def blind_rule_predictions(options: dict[str, str], section: str, question: int) -> dict[str, str]:
    """Return rule -> predicted letter. These rules use only option text."""
    predictions: dict[str, str] = {}
    letters = list("ABCD")

    lens = {letter: len(words(options[letter])) for letter in letters}
    max_len = max(lens.values())
    min_len = min(lens.values())
    max_letters = [k for k, v in lens.items() if v == max_len]
    min_letters = [k for k, v in lens.items() if v == min_len]
    if len(max_letters) == 1:
        predictions["choose_longest"] = max_letters[0]
    if len(min_letters) == 1:
        predictions["choose_shortest"] = min_letters[0]

    for feature, pattern in FEATURES.items():
        labs = [letter for letter in letters if has(pattern, options[letter])]
        if len(labs) == 1:
            predictions[f"choose_unique_{feature}"] = labs[0]
            # Also evaluate elimination-style rules by picking the first
            # remaining letter. Accuracy of elimination is computed separately.

    # Prefer moderate over extreme if exactly one moderate option and exactly
    # one or more extreme options exist.
    moderate = [letter for letter in letters if "moderate" in option_features(options[letter])]
    extreme = [letter for letter in letters if "extreme_bad" in option_features(options[letter])]
    if len(moderate) == 1 and moderate[0] not in extreme:
        predictions["choose_unique_moderate"] = moderate[0]

    # Section-position priors, based only on question number and option surface.
    if section == "A" and question in {4, 8}:
        labs = [letter for letter in letters if has(FEATURES["future"], options[letter]) or has(FEATURES["advice_plan"], options[letter])]
        if len(labs) == 1:
            predictions["A_last_choose_plan_future"] = labs[0]

    if section == "B" and question in {9, 12}:
        labs = [letter for letter in letters if has(FEATURES["research"], options[letter]) or has(r"\b(issue|problem|debate|question|main|topic|purpose)\b", options[letter])]
        if len(labs) == 1:
            predictions["B_first_choose_research_or_issue"] = labs[0]

    if section == "C" and question in {18, 21, 25}:
        labs = [letter for letter in letters if has(r"\b(essential|overall|main|long-term|in general|attitude|characteristic|focus|meaning|purpose)\b", options[letter])]
        if len(labs) == 1:
            predictions["C_late_choose_abstract_summary"] = labs[0]

    # Opposite-pair rules: if a positive and negative option coexist on one
    # dimension, do not blindly choose; score both directions as separate rules.
    pos_pat = r"\b(benefit|beneficial|advantage|improve|support|accept|successful|popular|effective|help|protect|respect|cooperative|healthy|appealing|opportunit(?:y|ies))\b"
    neg_pat = r"\b(harm|harmful|disadvantage|worse|oppose|reject|failure|unpopular|ineffective|hurt|risk|threat|conflict|passive|unhealthy|adversely|problem|crisis)\b"
    pos = [letter for letter in letters if has(pos_pat, options[letter])]
    neg = [letter for letter in letters if has(neg_pat, options[letter])]
    if len(pos) == 1 and len(neg) == 1:
        predictions["opposition_choose_positive"] = pos[0]
        predictions["opposition_choose_negative"] = neg[0]

    more = [letter for letter in letters if has(r"\b(more|higher|increase|larger|grow|growth|double|doubled|above)\b", options[letter])]
    less = [letter for letter in letters if has(r"\b(less|lower|decrease|reduce|reduced|smaller|decline|below|fewer)\b", options[letter])]
    if len(more) == 1 and len(less) == 1:
        predictions["opposition_choose_more"] = more[0]
        predictions["opposition_choose_less"] = less[0]

    return predictions


def evaluate_blind_rules(
    answer_key: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    with (OUT / "question_option_records.csv").open(encoding="utf-8-sig", newline="") as f:
        option_rows = list(csv.DictReader(f))
    answers = {(row["key"], row["question"]): row for row in answer_key if is_evaluable_answer_row(row)}

    examples: list[dict[str, str]] = []
    pred_stats: dict[str, Counter] = defaultdict(Counter)
    elim_stats: dict[str, Counter] = defaultdict(Counter)
    qnum_stats: dict[int, Counter] = defaultdict(Counter)

    for row in option_rows:
        question = row["question"]
        key = (row["key"], question)
        if key not in answers:
            continue
        options = split_options(row["raw_options"])
        if len(options) != 4:
            continue
        answer = answers[key]["answer"]
        section = row["section"]
        qnum = int(question)
        qnum_stats[qnum][answer] += 1

        predictions = blind_rule_predictions(options, section, qnum)
        for rule, pred in predictions.items():
            pred_stats[rule]["total"] += 1
            pred_stats[rule]["hit"] += int(pred == answer)
            if len([e for e in examples if e["rule"] == rule]) < 5:
                examples.append(
                    {
                        "rule": rule,
                        "key": row["key"],
                        "question": question,
                        "section": section,
                        "prediction": pred,
                        "answer": answer,
                        "hit": str(pred == answer),
                        "options": " | ".join(f"{letter}: {options[letter]}" for letter in "ABCD"),
                    }
                )

        # Elimination rules: if exactly one option has feature, evaluate
        # whether it is safe to eliminate it.
        for feature, pattern in FEATURES.items():
            labs = [letter for letter in "ABCD" if has(pattern, options[letter])]
            if len(labs) == 1:
                rule = f"eliminate_unique_{feature}"
                elim_stats[rule]["total"] += 1
                elim_stats[rule]["safe"] += int(labs[0] != answer)
        if len(max((len(words(options[letter])), letter) for letter in "ABCD")):
            pass

    rows = []
    for rule, stat in sorted(pred_stats.items()):
        total = stat["total"]
        hit = stat["hit"]
        rows.append(
            {
                "rule": rule,
                "type": "choose",
                "total": str(total),
                "hit": str(hit),
                "accuracy": f"{hit / total:.3f}" if total else "",
                "baseline": "0.250",
            }
        )
    for rule, stat in sorted(elim_stats.items()):
        total = stat["total"]
        safe = stat["safe"]
        rows.append(
            {
                "rule": rule,
                "type": "eliminate",
                "total": str(total),
                "hit": str(safe),
                "accuracy": f"{safe / total:.3f}" if total else "",
                "baseline": "0.750",
            }
        )

    qnum_rows: list[dict[str, str]] = []
    for qnum in sorted(qnum_stats):
        dist = qnum_stats[qnum]
        total = sum(dist.values())
        best_letter, best_count = max(dist.items(), key=lambda item: (item[1], item[0]))
        qnum_rows.append(
            {
                "question": str(qnum),
                "n": str(total),
                "best": best_letter,
                "hit": str(best_count),
                "accuracy": f"{best_count / total:.3f}" if total else "",
                "dist": str(dict(dist)),
            }
        )

    return rows, examples, option_rows, qnum_rows


def evaluate_signal_scan(answer_key: list[dict[str, str]]) -> list[dict[str, str]]:
    with (OUT / "question_option_records.csv").open(encoding="utf-8-sig", newline="") as f:
        option_rows = list(csv.DictReader(f))
    answers = {(row["key"], row["question"]): row for row in answer_key if is_evaluable_answer_row(row)}

    stats: dict[str, Counter] = defaultdict(Counter)
    section_stats: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))

    for row in option_rows:
        key = (row["key"], row["question"])
        if key not in answers:
            continue
        options = split_options(row["raw_options"])
        if len(options) != 4:
            continue
        answer = answers[key]["answer"]
        section = row["section"]

        for signal, pattern in SIGNAL_SCAN_PATTERNS.items():
            labs = [letter for letter in "ABCD" if has(pattern, options[letter])]
            if len(labs) != 1:
                continue
            hit = int(labs[0] == answer)
            stats[signal]["total"] += 1
            stats[signal]["hit"] += hit
            section_stats[signal][section]["total"] += 1
            section_stats[signal][section]["hit"] += hit

    rows: list[dict[str, str]] = []
    for signal in sorted(stats):
        total = stats[signal]["total"]
        hit = stats[signal]["hit"]
        row = {
            "signal": signal,
            "total": str(total),
            "hit": str(hit),
            "accuracy": f"{hit / total:.3f}" if total else "",
        }
        for section in "ABC":
            section_total = section_stats[signal][section]["total"]
            section_hit = section_stats[signal][section]["hit"]
            row[f"section_{section}"] = (
                f"{section_hit}/{section_total}={section_hit / section_total:.3f}"
                if section_total
                else ""
            )
        rows.append(row)
    return rows


def evaluate_similarity_pairs(
    answer_key: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with (OUT / "question_option_records.csv").open(encoding="utf-8-sig", newline="") as f:
        option_rows = list(csv.DictReader(f))
    answers = {(row["key"], row["question"]): row for row in answer_key if is_evaluable_answer_row(row)}

    clear_stats: dict[float, Counter] = defaultdict(Counter)
    section_stats: dict[float, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    pair_rows: list[dict[str, str]] = []

    for row in option_rows:
        key = (row["key"], row["question"])
        answer_row = answers.get(key)
        if not answer_row:
            continue
        options = split_options(row["raw_options"])
        if len(options) != 4:
            continue

        pair_scores: list[tuple[float, str, str, str]] = []
        for left in "ABCD":
            for right in "ABCD":
                if left >= right:
                    continue
                pair_scores.append(
                    (
                        option_similarity_score(options[left], options[right]),
                        left + right,
                        left,
                        right,
                    )
                )
        pair_scores.sort(reverse=True)
        top_score, top_pair, left, right = pair_scores[0]
        second_score, second_pair, *_rest = pair_scores[1]
        answer = answer_row["answer"]
        answer_in_pair = answer in top_pair
        mate = ""
        answer_shorter = ""
        answer_fewer_words = ""
        if answer_in_pair:
            mate = right if answer == left else left
            answer_shorter = str(compact_len(options[answer]) < compact_len(options[mate]))
            answer_fewer_words = str(len(content_words(options[answer])) < len(content_words(options[mate])))

        pair_rows.append(
            {
                "key": row["key"],
                "question": row["question"],
                "section": row["section"],
                "answer": answer,
                "top_pair": top_pair,
                "top_score": f"{top_score:.3f}",
                "second_pair": second_pair,
                "second_score": f"{second_score:.3f}",
                "margin": f"{top_score - second_score:.3f}",
                "answer_in_pair": str(answer_in_pair),
                "answer_mate": mate,
                "answer_shorter": answer_shorter,
                "answer_fewer_words": answer_fewer_words,
                "options": " | ".join(f"{letter}: {options[letter]}" for letter in "ABCD"),
            }
        )

        for threshold in [0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32]:
            if top_score < threshold:
                continue
            clear_stats[threshold]["clear"] += 1
            clear_stats[threshold]["in_pair"] += int(answer_in_pair)
            if answer_in_pair:
                clear_stats[threshold]["shorter"] += int(answer_shorter == "True")
                clear_stats[threshold]["fewer_words"] += int(answer_fewer_words == "True")
            section_stats[threshold][row["section"]]["clear"] += 1
            section_stats[threshold][row["section"]]["in_pair"] += int(answer_in_pair)

    threshold_rows: list[dict[str, str]] = []
    for threshold in [0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32]:
        stats = clear_stats[threshold]
        clear = stats["clear"]
        in_pair = stats["in_pair"]
        row = {
            "threshold": f"{threshold:.2f}",
            "clear": str(clear),
            "in_pair": str(in_pair),
            "in_pair_rate": f"{in_pair / clear:.3f}" if clear else "",
            "answer_shorter": str(stats["shorter"]),
            "answer_shorter_rate": f"{stats['shorter'] / in_pair:.3f}" if in_pair else "",
            "answer_fewer_words": str(stats["fewer_words"]),
            "answer_fewer_words_rate": f"{stats['fewer_words'] / in_pair:.3f}" if in_pair else "",
        }
        for section in "ABC":
            sec_clear = section_stats[threshold][section]["clear"]
            sec_in_pair = section_stats[threshold][section]["in_pair"]
            row[f"section_{section}"] = (
                f"{sec_in_pair}/{sec_clear}={sec_in_pair / sec_clear:.3f}"
                if sec_clear
                else ""
            )
        threshold_rows.append(row)

    return threshold_rows, pair_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Use already rebuilt column-text pages only; do not run OCR for missing pages.",
    )
    args = parser.parse_args()

    answer_key = rebuild_answer_key(cached_only=args.cached_only)
    write_csv(OUT / "listening_answer_key_rebuilt.csv", answer_key)
    full_closure_rows = build_full_closure_audit_rows(answer_key)
    write_csv(OUT / "listening_full_closure_audit.csv", full_closure_rows)
    answer_audit_rows = build_answer_audit_rows(answer_key)
    manual_audit_rows = build_manual_answer_audit_rows()
    write_csv(OUT / "listening_answer_key_audit.csv", answer_audit_rows)
    write_csv(OUT / "listening_answer_key_manual_audit.csv", manual_audit_rows)
    eval_rows, examples, _option_rows, qnum_rows = evaluate_blind_rules(answer_key)
    write_csv(OUT / "blind_guess_rule_eval.csv", eval_rows)
    write_csv(OUT / "blind_guess_rule_eval_high_clean.csv", eval_rows)
    write_csv(OUT / "blind_guess_rule_examples.csv", examples)
    write_csv(OUT / "blind_guess_rule_high_examples.csv", examples)
    write_csv(OUT / "blind_guess_qnum_priors_high.csv", qnum_rows)
    signal_rows = evaluate_signal_scan(answer_key)
    write_csv(OUT / "blind_guess_signal_scan.csv", signal_rows)
    similarity_rows, similarity_pair_rows = evaluate_similarity_pairs(answer_key)
    write_csv(OUT / "blind_guess_similarity_scan.csv", similarity_rows)
    write_csv(OUT / "blind_guess_similarity_pairs.csv", similarity_pair_rows)

    print(f"answer key rows: {len(answer_key)}")
    print(Counter(row["confidence"] for row in answer_key))
    print(f"full closure rows: {len(full_closure_rows)}")
    print(Counter(row["status"] for row in full_closure_rows))
    print(f"answer audit rows: {len(answer_audit_rows)}")
    print(f"manual audit rows: {len(manual_audit_rows)}")
    print(f"rule rows: {len(eval_rows)}")
    print(f"signal rows: {len(signal_rows)}")
    print(f"similarity rows: {len(similarity_rows)}")
    for row in sorted(eval_rows, key=lambda r: (r["type"], -int(r["total"]), r["rule"]))[:20]:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
