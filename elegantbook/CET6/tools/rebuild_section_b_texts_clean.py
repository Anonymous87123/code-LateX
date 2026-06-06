from pathlib import Path


OUT = Path(__file__).resolve().parent.parent / "cet 6" / "_analysis_output" / "section_b_texts"


TEXTS = {
    "2016年6月英语六级真题(第1套).txt": {
        "title": "Can Societies Be Rich and Green?",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2016年6月英语六级真题(第2套).txt": {
        "title": "Reform and Medical Costs",
        "letters": list("ABCDEFGHIJKLMNOPQ"),
    },
    "2016年6月英语六级真题(第3套).txt": {
        "title": "The Changing Generation",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2016年12月英语六级真题(第1套).txt": {
        "title": "Are We in an Innovation Lull?",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2016年12月英语六级真题(第2套).txt": {
        "title": "Countries Rush for Upper Hand in Antarctica",
        "letters": list("ABCDEFGHIJKLMNOPQ"),
    },
    "2016年12月英语六级真题(第3套).txt": {
        "title": "The American Workplace Is Broken. Here's How We Can Start Fixing It.",
        "letters": list("ABCDEFGHIJKLM"),
    },
    "2017年6月英语六级真题(第1套).txt": {
        "title": "The Price of Oil and the Price of Carbon",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2017年6月英语六级真题(第2套).txt": {
        "title": "Elite Math Competitions Struggle to Diversify Their Talent Pool",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2017年6月英语六级真题(第3套).txt": {
        "title": "Rich Children and Poor Ones Are Raised Very Differently",
        "letters": list("ABCDEFGHIJKLMNOPQ"),
    },
    "2017年12月英语六级真题(第1套).txt": {
        "title": "Who's Really Addicting You to Technology?",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2017年12月英语六级真题(第2套).txt": {
        "title": "Data sharing: An open mind on open data",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2017年12月英语六级真题(第3套).txt": {
        "title": "Apple's Stance Highlights a More Confrontational Tech Industry",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2018年6月英语六级真题(第1套).txt": {
        "title": "Peer Pressure Has a Positive Side",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2018年6月英语六级真题(第2套).txt": {
        "title": "Grow Plants Without Water",
        "letters": list("ABCDEFGHIJK"),
    },
    "2018年6月英语六级真题(第3套).txt": {
        "title": "In the real world, nobody cares that you went to an Ivy League school",
        "letters": list("ABCDEFGHIJKLMN"),
    },
    "2018年12月英语六级真题(第1套).txt": {
        "title": "Do Parents Invade Children's Privacy When They Post Photos Online?",
        "letters": list("ABCDEFGHIJKLMN"),
    },
    "2018年12月英语六级真题(第2套).txt": {
        "title": "A Pioneering Woman of Science Re-Emerges after 300 Years",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2018年12月英语六级真题(第3套).txt": {
        "title": "Resilience Is About How You Recharge, Not How You Endure",
        "letters": list("ABCDEFGHIJKLM"),
    },
    "2019年6月英语六级真题(第1套).txt": {
        "title": "The Best Retailers Combine Bricks and Clicks",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2019年6月英语六级真题(第2套).txt": {
        "title": "Companies Are Working with Consumers to Reduce Waste",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2019年6月英语六级真题(第3套).txt": {
        "title": "The future of personal satellite technology is here-are we ready for it?",
        "letters": list("ABCDEFGHIJKLM"),
    },
    "2019年12月英语六级真题(第1套).txt": {
        "title": "Increased Screen Time and Wellbeing Decline in Youth",
        "letters": list("ABCDEFGHIJ"),
    },
    "2019年12月英语六级真题(第2套).txt": {
        "title": "How Much Protein Do You Really Need?",
        "letters": list("ABCDEFGHIJKLMN"),
    },
    "2019年12月英语六级真题(第3套).txt": {
        "title": "Why More Farmers Are Making The Switch to Grass-Fed Meat and Dairy",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2020年9月英语六级真题(第1套).txt": {
        "title": "Six Potential Brain Benefits of Bilingual Education",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2020年9月英语六级真题(第2套).txt": {
        "title": "How Telemedicine Is Transforming Healthcare",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2020年12月英语六级真题(第1套).txt": {
        "title": "The Challenges for Artificial Intelligence in Agriculture",
        "letters": list("ABCDEFGHIJKLMNOPQR"),
    },
    "2020年12月英语六级真题(第2套).txt": {
        "title": "Slow Hope",
        "letters": list("ABCDEFGHIJK"),
    },
    "2020年12月英语六级真题(第3套).txt": {
        "title": "Why lifelong learning is the international passport to success",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2021年6月英语六级真题(第1套).txt": {
        "title": "How Marconi Gave Us the Wireless World",
        "letters": list("ABCDEFGHIJK"),
    },
    "2021年6月英语六级真题(第2套).txt": {
        "title": "France's beloved cathedral only minutes away from complete destruction",
        "letters": list("ABCDEFGHIJK"),
    },
    "2021年6月英语六级真题(第3套).txt": {
        "title": "What Are the Ethics of CGI Actors-And Will They Replace Real Ones?",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2021年12月英语六级真题(第1套).txt": {
        "title": "No one in fashion is surprised that Burberry burnt 28 million of stock",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2021年12月英语六级真题(第2套).txt": {
        "title": "Do music lessons really make children smarter?",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2021年12月英语六级真题(第3套).txt": {
        "title": "Why facts don't change our minds",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
}


def build_text(title: str, letters: list[str]) -> str:
    lines = [
        "Section B",
        "Directions: In this section, you are going to read a passage with ten statements attached to it. Each statement contains information given in one of the paragraphs. Identify the paragraph from which the information is derived. You may choose a paragraph more than once. Each paragraph is marked with a letter. Answer the questions by marking the corresponding letter on Answer Sheet 2.",
        title,
    ]
    for letter in letters:
        lines.append(f"{letter}) Placeholder paragraph {letter}.")
    lines.extend(
        [
            "36. Placeholder statement.",
            "37. Placeholder statement.",
            "38. Placeholder statement.",
            "39. Placeholder statement.",
            "40. Placeholder statement.",
            "41. Placeholder statement.",
            "42. Placeholder statement.",
            "43. Placeholder statement.",
            "44. Placeholder statement.",
            "45. Placeholder statement.",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, spec in TEXTS.items():
        (OUT / name).write_text(build_text(spec["title"], spec["letters"]), encoding="utf-8")


if __name__ == "__main__":
    main()
