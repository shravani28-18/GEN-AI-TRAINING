# PashuSeva – Prompt Comparison Report

## 1. Objective

The objective of this evaluation is to compare two prompt versions for answering farmer questions using available PashuSeva records.

## 2. Prompt Versions

### Prompt Version A – Basic Prompt
- Uses short and simple instructions.
- Answers questions using the provided records.
- Focuses on concise responses.
- Has fewer detailed safety instructions.

### Prompt Version B – Detailed Prompt
- Uses detailed instructions.
- Focuses on farmer-friendly explanations.
- Avoids unsupported information and assumptions.
- Includes safety instructions for animal health questions.
- Requires structured JSON output.

## 3. Dataset

- Project: PashuSeva
- Total sample questions: 10
- Available records: 7
- Main topics: Fodder and animal feeding
- Evaluation method: Both prompts are tested on the same questions using the same retrieved context.

## 4. Evaluation Criteria

1. Answer accuracy
2. Relevance to the question
3. Clarity and simplicity
4. Use of available records
5. Handling of unavailable information
6. Avoidance of unsupported advice

## 5. Evaluation Results

The responses from both prompt versions are saved in `eval/results.json`.

The evaluation covers all 10 sample questions. A manual review of the generated answers is required before deciding which prompt performs better.

## 6. Observations

- Both prompt versions use the same PashuSeva records as context.
- Prompt Version A provides a basic response structure.
- Prompt Version B includes more detailed instructions and safety guidance.
- The vaccination question tests whether the assistant correctly identifies unavailable information.
- The dataset currently focuses mainly on fodder and feeding topics.
### Question 6 – Vaccination Schedule

- Prompt A correctly stated that vaccination information was unavailable.
- Prompt B also stated that vaccination information was unavailable.
- Neither prompt invented a vaccination schedule.
- Prompt B returned structured JSON output.
- However, Prompt B assigned high confidence despite unavailable information.
- The confidence value should be low when the required records are missing.
- A recommendation to consult a qualified veterinarian would improve safety.

### Improvement Identified

Prompt B needs better confidence handling for questions that cannot be answered using available records.

## 7. Conclusion

Prompt Version A and Prompt Version B were tested using the same 10 sample questions.

Prompt Version B is designed to provide more structured and safety-focused responses. However, the final selection should be based on manual evaluation of the actual generated answers rather than assumptions.

## 8. Output File

`eval/results.json` contains the generated answers from both prompt versions for further review.