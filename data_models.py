from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

##############################################################################
# (1) Assessment
##############################################################################

class MatchTag(str, Enum):
    yes = "Yes"
    no = "No"

class Criterion(BaseModel):
    text: str = Field(description="Formulation of the criterion")
    match: MatchTag = Field(description="Criterion match tag")
    explanation: str = Field(description="Explanation why the answer matches/doesn't match criterion")

class Assessment(BaseModel):
    criteria: List[Criterion] = Field(description="List of criterions")
    final_thoughts: Optional[str] = Field(description="Summary of the answer assessment against all criteria", default=None)
    score: Optional[float] = Field(description="Score assigned to the answer given the criteria match", default=None)


##############################################################################
# (2) Validation dataset
##############################################################################

class Answer(BaseModel):
    id: int = Field(description="Answer id")
    text: str = Field(description="Answer text")
    score: float = Field(description="Score assigned to the answer by methodologist")
    explanation: str = Field(description="Explanation of the score given by the methodologist")

class Question(BaseModel):
    id: int = Field(description="Question id")
    text: str = Field(description="Question text")
    answers: List[Answer] = Field(description="List of answers to the question")

class ValidationDataset(BaseModel):
    questions: List[Question] = Field(description="List of questions")