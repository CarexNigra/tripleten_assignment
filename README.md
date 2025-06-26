# Task

The task was following

```
The student was asked the following question: 

"Imagine you are a data scientist at a mid-sized e-commerce 
company aiming to boost customer retention. Describe how LTV insights
can help formulate actionable customer retention strategies for this company."

There is some model that scores students' answers from 0 to 1. 
We need to reverse engineer and build the same model that would return 
the same scores on such answers of students given the provided 
    – answer examples
    – their scores assigned by methodologists
    – explanation of the scores by methodologists
```
![Setup](./docs/setup.png)

# Approaches
I developped two approaches

## Approach 1
![Approach 1](./docs/approach_1.png)

Pros:
* Simple: 1 system prompt + 1 user prompt (with answer)

Cons:
* Each time we run this setting, criteria may differ (which results into different criteria for the same question)

## Approach 2
![Approach 2](./docs/approach_2.png)

Pros:
* Single set of assessment criteria per question => consistent scoring of all answers
* Assessment criteria generated automatically based on examples manually labeled by methodologists

Cons:
* More complex: 2 steps + more calls required

Extras:
* Automatic generation of validation dataset based on examples manually labeled by methodologists

![Validation](./docs/validation.png)


Considerations:
* Model output scores may differ from run to run. It may be good to run scoring multiple times, do majority voting and use this score to compare with reference score
* Try to explicitly define how number of matched criteria translate to score

# Next steps (improvments)
1. Implement async openai calls to speed up  answers' processing (parallelization). But should be limited to not face the OpenAIs API rate limits
2. Implement majority voting for scorers  to increase scores stability
3. Add logic to the scoring prompt that "deterministically" translates number of matched criteria into score
4. Store question evaluation criteria in a map to avoid recomputing it for each evaluation call (in-memory storage in inference)
5. Clean up code structure: type hints, classes, unit tests, etc.

