from pathlib import Path
import json
import pandas as pd
import requests
import json

from configs.configs import API_KEY, API_URL

##############################################################################
# (1) Call open_ia
##############################################################################

def call_openai_api(user_prompt, system_instructions):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    json_response = response.json()
    content = json_response.get("choices", [{}])[0].get("message", {}).get("content", "")
    return content


##############################################################################
# (2) Visualize assessments and criteria
##############################################################################

def assessments_to_df(assessments, question, answer):
    records = []
    for a in assessments:
        records.append({
            "question": question, 
            "answer": answer,
            "criterions": [c.model_dump() for c in a.criteria],
            "final_thought": a.final_thoughts,
            "score": a.score
        })
    df = pd.DataFrame(records)
    return df


def criterions_to_df(assessments):
    records = []
    i = 0
    for a in assessments:
        criterions = [c.model_dump() for c in a.criteria]
        for c in criterions:
            records.append({
                "answer_id": i,
                "criterion_text": c['text'],
                "match": c['match'].value,
                "explanation": c['explanation']
            })
        i += 1
    df = pd.DataFrame(records)
    return df


##############################################################################
# (3) Saving
##############################################################################

def save_dataset(file_path, dataset):
    path = Path(file_path) 
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)