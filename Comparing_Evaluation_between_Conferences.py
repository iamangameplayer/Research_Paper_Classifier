import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


input_folder = # Folder containing parsed papers of reference conferences

output_file = # Output file to present the observable characteristics of the conferences


def load_conference_papers(folder_path):

    conferences = {}

    for conference_name in os.listdir(folder_path):

        conference_path = os.path.join(
            folder_path,
            conference_name
        )

        if not os.path.isdir(conference_path):
            continue

        papers = {}

        for filename in os.listdir(conference_path):

            if filename.endswith(".json"):

                file_path = os.path.join(
                    conference_path,
                    filename
                )

                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        papers[filename] = json.load(f)
                    except json.decoder.JSONDecodeError as e:
                        print(f"Corrupt JSON File detected : {filename}")
                        print(f"Error Details : {e}")
                        raise e

        conferences[conference_name] = papers

    return conferences


conference_data = load_conference_papers(input_folder)


conference_prompt = """
You are an expert research-paper and academic-conference analysis assistant.

You are given research-paper analyses belonging to different conferences.

Each conference contains a small set of papers that were accepted by
that conference.

Your task is to identify the observable characteristics and patterns
of the papers associated with each conference.

IMPORTANT:

- Use ONLY the supplied JSON analyses.
- Do NOT invent conference requirements.
- Do NOT claim that a characteristic is an official conference rule
  unless it is explicitly present in the supplied information.
- Do NOT rank the conferences.
- Do NOT decide which conference is better.
- Do NOT predict acceptance.
- Do NOT assume that two papers completely represent a conference.
- There are only two papers per conference, so findings must be treated
  as observed patterns, not definitive conference requirements.
- If evidence is insufficient, write "Insufficient evidence".
- Focus on characteristics that can actually be observed from the
  supplied research-paper analyses.

The 15 research-quality criteria are:

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


For EACH conference, analyze:

1. Conference_Name

2. Number_of_Papers

3. Common_Research_Problems

Identify recurring types of research problems.

4. Common_Research_Gaps

Identify recurring types of research gaps.

5. Common_Topics_or_Research_Areas

Identify the research areas represented by the papers.

6. Common_Methodologies

Identify recurring methodological approaches.

7. Common_Datasets

Identify recurring dataset characteristics or dataset types.

8. Common_Experimental_Approaches

Identify recurring experimental patterns.

9. Common_Baseline_Approaches

Identify how papers compare against existing methods.

10. Common_Evaluation_Metrics

Identify recurring evaluation metrics.

11. Common_Contribution_Patterns

Identify what kinds of contributions the papers make.

12. Common_Novelty_Patterns

Identify observable forms of novelty.

13. Common_Quality_Characteristics

Identify characteristics shared by the papers.

14. Average_Criterion_Scores

For each of the 15 criteria, calculate the average score across
the papers belonging to that conference.

15. Recurring_Strengths

Identify characteristics that appear consistently across the papers.

16. Recurring_Weaknesses

Identify characteristics that appear weaker or less developed.

17. Conference_Profile

Create a concise evidence-based profile describing the type of
research represented by the supplied papers.

18. Observable_Alignment_Characteristics

List characteristics that a NEW paper could be checked against
when determining whether it resembles the research represented
by this conference's supplied papers.


After analyzing each conference individually, provide:

OVERALL_CONFERENCE_COMPARISON

For every research characteristic, compare how it appears across
the different conferences.

Do NOT rank conferences.

Instead, produce a structured comparison showing:

- characteristic
- conference
- observed pattern
- evidence strength

Then identify:

1. Distinctive_Characteristics

Characteristics that appear particularly characteristic of one
conference's supplied papers compared with the other supplied
conference groups.

2. Shared_Characteristics

Characteristics that appear across multiple conferences.

3. Conference_Differences

Important observable differences between conference groups.

4. Conference_Overlap

Areas where the conferences appear similar.

5. Limitations

Explain why two papers per conference are insufficient to establish
official or general conference requirements.

Return ONLY valid JSON.
"""


response = client.chat.completions.create(

    model="qwen/qwen3-30b-a3b-instruct-2507",

    messages=[
        {
            "role": "system",
            "content": conference_prompt
        },
        {
            "role": "user",
            "content": json.dumps(
                conference_data,
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


print("\nConference analysis completed.")
print(f"Saved to: {output_file}")