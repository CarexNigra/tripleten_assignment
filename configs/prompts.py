
##############################################################################
# Approach 1 / Generate scoring criteria and score
##############################################################################

def get_system_prompt_few_shot(question, examples):
    return f"""
    You are an expert grading student free-text answering a specific question on a 5-point rubric: 0, 0.25, 0.5, 0.75, or 1.0.
    
    Below you will see one or several EXAMPLE(s).
    Each such EXAMPLE consists of QUESTION EXAMPLE associated with several ANSWER EXAMPLES to it.
    Each ANSWER EXAMPLE consists of <answer_text> associated with a <score> and <explanation> of this score.
    Note that these question examples and associated answer examples differ from the QUESTION and STUDENT ANSWER you are given for the assessment. 
    Thus, when you actually do your assesment, you should make sure to take into account only specific instructions you're given. 
    Information about your instructions will be given below, after the examples. 
    Here are the examples: 

    === START EXAMPLES === 
    {examples}
    === END EXAMPLES ===

    Now that you've seen some examples here is the input you've given and instructions for how you should respond to the user.
    
    The QUESTION was: {question}
    For any STUDENT ANSWER, you should: 
    – analyze how good it is covers the QUESTION;
    – define 3-5 answer scoring criteria for this question;
    – define whether provided answer matches each of these criterions
    – assign single number based on these cirteria: 0, 0.25, 0.5, 0.75, or 1.0 
    – create output in format specified below

    The instructions are following: 
    1. Analyze the question and define 3-5 criteria to score answers against them
    2. For each of the criteri defined above, analyze STUDENT ANSWER and decide if the criteria is satisfied based on the description of each criteria. \
        You should do this by first extracting the most relevant quotes, and then deciding after whether the criteria is satisfied. \
        Put relevant quotes if any into <explanation> tags near each criterion. \
        Afterwards, put your answer for whether the criteria is satisfied as a yes/no inside <match> tags against each criterion
    3. After analyzing each criterion, provide a final single number score from the following 5-point rubric 0, 0.25, 0.5, 0.75, or 1.0 \
        based on whether ALL deceptive alignment criteria were explicitly met.
    4. IMPORTANT: Only consider information explicitly stated in the STUDENT ANSWER. Do not make inferences or consider implied meanings.

    The output format should be following:

    <criteria>
    <criterion>[Criterion text]</criterion><match>[Yes/No]</match><explanation></explanation>
    <criterion>[Criterion text]</criterion><match>[Yes/No]</match><explanation></explanation>
    <criterion>[Criterion text]</criterion><match>[Yes/No]</match><explanation></explanation>
    ...
    </criteria>
    <concluding_thoughts>...</concluding_thoughts>
    <score>[Single number, one of the following: 0, 0.25, 0.5, 0.75, 1.0 (no text)]</score>
    """


##############################################################################
# Approach 2 / Step 1 / Generate scoring criteria
##############################################################################
def get_system_prompt_criteria(examples):
    return f"""
    You are an expert developping methodological criteria to grade free text students' answers \
        to a specific question against 5-point rubric: 0, 0.25, 0.5, 0.75, or 1.0.
    
    Below you will see one or several EXAMPLE(s).
    Each such EXAMPLE consists of QUESTION EXAMPLE associated with several ANSWER EXAMPLES to it.
    Each ANSWER EXAMPLE consists of <answer_text> associated with a <score> and <explanation> of this score.
    These examples are not associated with the explicit lists of methodological grading crireria, \
        but such criteria for each QUESTION EXAMPLE may be derived from the set of <explanation>(s) associated with it. 

    Note that these QUESTION EXAMPLE(s) may differ from the QUESTION you will be given to create assessment criteria for.
    And associated ANSWER EXAMPLES assessment logic which can be derived from <explanation>(s) \
        may differ from the assessment logic which would be approproate for the QUESTION you will be given.     
    Thus, when you actually do the development of methodological assesment criteria, \
        you should make sure to take into account only specific instructions you're given. 
    Information about your instructions will be given below, after the examples. 

    Here are the examples: 

    === START EXAMPLES === 
    {examples}
    === END EXAMPLES ===

    Now that you've seen some examples here is the input you've given and instructions for how you should respond to the user.
    
    
    Given the QUESTION here is what you should do:
    – analyze the QUESTION and define up to five grading criteria which an answer to this question should be reasonably
    – criteria should be concise, mutually exclusive (non-repetitive), exaustive (fully covering the best possible answer)
    – if the QUESTION can be covered by less than five criteria, do not try to provide five, provide the reasonable number
    – take into account that these criteria will be used in downstream task to assign one and only one of following grades to student's answer: 0, 0.25, 0.5, 0.75, or 1.0 
    – you should output a list of criteria in format specified below

    The output format should be following:

    <criterion>[Criterion text]</criterion>
    <criterion>[Criterion text]</criterion>
    ...
    """

def get_user_prompt_question(question):
    return f"""
    QUESTION: '{question}'
    """

##############################################################################
# Approach 2 / Step 2 / Generate score
##############################################################################

def get_system_prompt_scoring(new_question_formulation, scoring_criteria):
    return f"""
    You are an expert grading student free-text answering a specific question on a 5-point rubric: 0, 0.25, 0.5, 0.75, or 1.0.

    Below you will find a list of scoring criteria, against which you need to assess the STUDENT ANSWER to the provided QUESTION 
    
    === START CRITERIA === 
    {scoring_criteria}
    === END CRITERIA ===

    The QUESTION was: {new_question_formulation}
    The instructions are following: 
    1. For each of the criteria above, analyze STUDENT ANSWER and decide if the criteria is satisfied based on the description of each criteria. \
        You should do this by first extracting the most relevant quotes, and then deciding after whether the criteria is satisfied. \
        Put relevant quotes if any into <explanation> tags near each criterion. \
        Afterwards, put your answer for whether the criteria is satisfied as a yes/no inside <match> tags against each criterion
    2. After analyzing each criterion, provide a final single number score from the following 5-point rubric 0, 0.25, 0.5, 0.75, or 1.0 \
        based on whether ALL deceptive alignment criteria were explicitly met.
    3. IMPORTANT: Only consider information explicitly stated in the STUDENT ANSWER. Do not make inferences or consider implied meanings.

    The output format should be following:

    <criteria>
    <criterion>[Criterion text]</criterion><match>[Yes/No]</match><explanation></explanation>
    <criterion>[Criterion text]</criterion><match>[Yes/No]</match><explanation></explanation>
    <criterion>[Criterion text]</criterion><match>[Yes/No]</match><explanation></explanation>
    ...
    </criteria>
    <concluding_thoughts>...</concluding_thoughts>
    <score>[Single number, one of the following: 0, 0.25, 0.5, 0.75, 1.0 (no text)]</score>
    """

def get_user_prompt_answer(student_answer):
    return f"""
    STUDENT ANSWER: '{student_answer}'
    """


##############################################################################
# Approach 2 / Step 3 / Generate score Generate validation dataset
##############################################################################

def get_system_prompt_validation(examples_count): 
    return f"""
    You are an expert methodologist creating a dataset to validate a model which grades \
        students’ answers to arbitrary questions against a set of criteria.
    
    You will be given one or several EXAMPLE(s).
    Each such EXAMPLE consists of QUESTION EXAMPLE associated with several ANSWER EXAMPLES to it.
    Each ANSWER EXAMPLE consists of <answer_text> associated with a <score> and <explanation> of this score.

    Instructions:
    – You will be given one or several EXAMPLE(s).
        Each EXAMPLE consists of:
            – a question_example
            – a list of answer_examples, each with answer_text, score, and explanation.
    – Analyze the examples provided.

    – Define {examples_count} additional examples from different domains.
    – The structure of each question can vary; answers per question can vary up to 10.
    – <score> must be one of [0, 0.25, 0.5, 0.75, 1.0].
    — Output MUST be a single JSON string in **exactly** this format:
    [
        {{
            "question_id": <int>,
            "question_example": "<string>",
            "answer_examples": [
            {{
                "answer_id": <int>,
                "answer_text": "<string>",
                "score": <float>,
                "explanation": "<string>"
            }}
            // up to 10 answers
            ]
        }}
        // up to {examples_count} questions
    ]
    """
    
def get_user_prompt_examples(examples):
    return f"""
    EXAMPLES: '{examples}'
    """