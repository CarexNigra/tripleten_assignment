import pandas as pd

from src.helpers import call_openai_api

from configs.prompts import (
    get_system_prompt_few_shot,
    get_user_prompt_answer, 
    get_user_prompt_question,
    get_system_prompt_criteria, 
    get_system_prompt_scoring,
    )
from src.parser import assessment_parser



def make_full_assessment_few_shot(question, answer, examples_for_prompt):
    system_prompt = get_system_prompt_few_shot(question, examples_for_prompt)
    user_prompt = get_user_prompt_answer(answer)
    assessment_raw = call_openai_api(user_prompt, system_prompt)
    assessment = assessment_parser(assessment_raw)
    return assessment


def make_full_assessment_two_steps(question, answer, examples_for_prompt):

    # Generate criteria # TODO: optimize = question-based lookup
    system_prompt_criteria = get_system_prompt_criteria(examples_for_prompt)
    user_prompt_criteria = get_user_prompt_question(question)
    criteria = call_openai_api(user_prompt_criteria, system_prompt_criteria)

    # Answer assessment
    system_prompt_scoring = get_system_prompt_scoring(question, criteria)
    user_prompt_scoring = get_user_prompt_answer(answer)
    assessment_raw = call_openai_api(user_prompt_scoring, system_prompt_scoring)
    assessment = assessment_parser(assessment_raw)
    
    return assessment
    


def validate_model(validation_dataset, number_of_questions_to_process, examples_for_prompt):

    criteria_df_data = []
    validation_df_data = []

    if not number_of_questions_to_process:
        number_of_questions_to_process = len(validation_dataset.questions) 

    # (1) For each question run criteria generation
    system_prompt_criteria = get_system_prompt_criteria(examples_for_prompt)
    
    for q in validation_dataset.questions[:number_of_questions_to_process]:    
        q_id = q.id
        q_text = q.text
        q_answers = q.answers

        user_prompt_criteria = get_user_prompt_question(q_text)
        criteria = call_openai_api(user_prompt_criteria, system_prompt_criteria)

        criteria_df_data.append({
            "question_id": q_id,
            "question_text": q_text,
            "criteria": criteria
        })

        # (2) Score each answer against the criteria
        for a in q_answers:
            a_id = a.id
            a_text = a.text
            a_real_score = a.score

            system_prompt_scoring = get_system_prompt_scoring(q_text, criteria)
            user_prompt_scoring = get_user_prompt_answer(a_text)
            scoring = call_openai_api(user_prompt_scoring, system_prompt_scoring)
            
            # parse assessment
            assessment = assessment_parser(scoring)
            assessed_score = assessment.score
            assessed_criteria = [c.match.value for c in assessment.criteria]
            score_explanation = assessment.final_thoughts

            # create df
            validation_df_data.append({
                "question_id": q_id,
                "answer_id": a_id,
                "answer_text": a_text,
                "score_real": a_real_score,
                "score_assessed": assessed_score,
                "criteria match": assessed_criteria,
                "score_explanation": score_explanation
            })

    criteria_df = pd.DataFrame(criteria_df_data)
    criteria_df['criteria'] = criteria_df['criteria'].str.findall(r'<criterion>(.*?)</criterion>')
    criteria_df_exploded = criteria_df.explode('criteria').reset_index(drop=True)

    validation_df = pd.DataFrame(validation_df_data)
    validation_df['score_match'] = (validation_df['score_real'] == validation_df['score_assessed'])

    return criteria_df_exploded, validation_df