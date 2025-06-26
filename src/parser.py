import re
import json

import xml.etree.ElementTree as ET
from data_models import Assessment, Criterion, MatchTag, Answer, Question, ValidationDataset


def assessment_parser(output: str) -> Assessment:
    """
    Parses an LLM output string into an Assessment object.
    """
    # XML parsing
    wrapped = f"<root>{output}</root>"
    root = ET.fromstring(wrapped)

    # Parse criteria
    criteria = root.find(".//criteria")
    criteria_list = []
    if criteria is not None:
        children = list(criteria)
        for i in range(0, len(children), 3):
            crit = children[i]
            match = children[i + 1]
            expl = children[i + 2]
            criteria_list.append(
                Criterion(
                    text=(crit.text or "").strip(),
                    match=MatchTag((match.text or "").strip()),
                    explanation=(expl.text or "").strip(),
                )
            )

    # Parse concluding thoughts
    thoughts = root.find(".//concluding_thoughts")
    final_thoughts = (thoughts.text or "").strip() if thoughts is not None else None

    # Parse score
    score = root.find(".//score")
    score = float((score.text or "").strip()) if score is not None else None

    return Assessment(criteria=criteria_list, final_thoughts=final_thoughts, score=score)


def validation_dataset_parser(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    questions = []
    for q in raw_data:
        answers = [
            Answer(
                id=ans["answer_id"],
                text=ans["answer_text"],
                score=ans["score"],
                explanation=ans["explanation"]
            )
            for ans in q["answer_examples"]
        ]
        question = Question(
            id=q["question_id"],
            text=q["question_example"],
            answers=answers
        )
        questions.append(question)

    dataset = ValidationDataset(questions=questions)
    return dataset


def clean_validation_dataset(dataset):
    cleaned = re.sub(r'```(?:json)?\s*', '', dataset)  
    cleaned = cleaned.replace('```', '') 
    cleaned = cleaned.strip()
    dataset_cleaned = json.loads(cleaned)
    return dataset_cleaned

