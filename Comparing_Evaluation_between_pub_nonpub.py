import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


publishable_folder = r"C:\Users\nagas\Desktop\IIT\Publishable_Results_JSON_Without_Conferences"
non_publishable_folder = r"C:\Users\nagas\Desktop\IIT\Non_Publishable_Results_JSON"

output_file = r"C:\Users\nagas\Desktop\IIT\Publishability_Comparison.json"



def load_json_folder(folder_path):
    papers = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    papers[filename] = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    print(f"❌ Corrupt JSON file detected: {filename}")
                    print(f"   Error details: {e}")
                    raise e

    return papers

publishable_papers = load_json_folder(publishable_folder)
non_publishable_papers = load_json_folder(non_publishable_folder)


comparison_prompt = """
You are an expert research-methodology analysis assistant.

You are given two groups of research-paper analyses.

GROUP 1:
Publishable papers

GROUP 2:
Non-publishable papers

Each paper has already been independently analyzed using the same
15 research-quality criteria.

Your task is to compare the two groups and identify patterns that
distinguish them.

IMPORTANT:

- Do NOT analyze the original papers.
- Use ONLY the JSON analyses provided.
- Do NOT invent information.
- Do NOT assume that a characteristic causes publishability.
- Treat the findings as patterns or associations observed in this
  small dataset.
- There are only 10 publishable papers and 5 non-publishable papers.
- Do not overgeneralize the findings to all research papers.
- If evidence is insufficient, explicitly say so.

The 15 criteria are:

1. Research Problem
2. Research Gap
3. Novelty
4. Objectives
5. Literature Review
6. Methodology Rigor
7. Dataset Quality
8. Experimental Validation
9. Baseline Comparison
10. Evaluation Metrics
11. Results Quality
12. Statistical Validation
13. Reproducibility
14. Limitations
15. Overall Research Contribution


For EACH criterion, determine:

- Publishable_Average_Score
- Non_Publishable_Average_Score
- Score_Difference
- Publishable_Pattern
- Non_Publishable_Pattern
- Distinguishing_Value
- Evidence_Summary


For Distinguishing_Value use ONLY:

"Strong"
"Moderate"
"Weak"
"None"


Then provide an overall analysis containing:

1. Strong_Publishability_Indicators

Characteristics that occur substantially more strongly or consistently
in the publishable group.

2. Moderate_Publishability_Indicators

Characteristics that show some association with the publishable group
but are not consistently strong.

3. Weak_or_Non_Distinguishing_Factors

Characteristics that do not clearly separate the two groups.

4. Non_Publishable_Patterns

Recurring weaknesses or characteristics observed in the
non-publishable group.

5. Most_Important_Observed_Differences

Summarize the most notable differences between the two groups.

6. Potential_Publishability_Rubric

Create a preliminary evidence-based rubric that could later be used
to analyze a new research paper.

Do NOT assign an arbitrary final "publishable" threshold yet.
We are only identifying the characteristics that may be useful.

7. Dataset_Limitations

Explain the limitations of drawing conclusions from only
10 publishable and 5 non-publishable papers.

Return ONLY valid JSON.
"""


comparison_data = {
    "Publishable_Papers": publishable_papers,
    "Non_Publishable_Papers": non_publishable_papers
}


response = client.chat.completions.create(
    model="qwen/qwen3-30b-a3b-instruct-2507",

    messages=[
        {
            "role": "system",
            "content": comparison_prompt
        },
        {
            "role": "user",
            "content": json.dumps(
                comparison_data,
                indent=2
            )
        }
    ],

    temperature=0,
    max_tokens=8000
)


result = response.choices[0].message.content


with open(output_file, "w", encoding="utf-8") as f:
    f.write(result)


print(f"\nComparison completed.")
print(f"Saved to: {output_file}")