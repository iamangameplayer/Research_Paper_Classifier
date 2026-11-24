import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

prompt = """
You are an expert research-paper analysis assistant specializing in
academic research quality and conference suitability.

You will be given a research paper that has already been accepted
into a specific conference. The conference name is represented by
the folder in which the paper is stored.

Your task is to analyze the paper and identify the characteristics
that may explain why the paper was suitable for and accepted by
that conference.

IMPORTANT:
- Do not invent information.
- Use only information present in the paper.
- Do not assume that acceptance guarantees scientific quality.
- Do not claim that any single characteristic guarantees acceptance.
- The dataset is small, so treat your findings as observed patterns,
  not universal rules.
- Do not compare this paper with papers from other conferences unless
  such papers are explicitly provided.
- Do not simply say that the paper is "good" or "high quality".
  Identify concrete characteristics supported by evidence.

Evaluate the following criteria:

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

For each criterion provide:

- score: integer from 0 to 5
- evidence: specific evidence from the paper
- explanation: brief explanation of the score

Scoring:

0 = Completely absent
1 = Very weak
2 = Weak
3 = Moderate
4 = Strong
5 = Very strong

If information is not present in the paper,
write "Not found" rather than guessing.

After evaluating the 15 criteria, provide a separate section called
"Conference_Suitability_Analysis".

In this section identify:

1. Conference_Relevant_Topics
   - What research areas, subjects, techniques, or applications
     in the paper appear relevant to the conference?

2. Research_Focus
   - What is the main research focus of the paper?

3. Technical_Characteristics
   - What technical approaches, models, algorithms, datasets,
     experiments, or methodologies are used?

4. Contribution_Characteristics
   - What does the paper contribute to its research area?

5. Quality_Characteristics
   - What characteristics of the paper indicate research maturity
     or quality?

6. Acceptance_Alignment
   - Based only on the paper and the fact that it was accepted into
     this conference, identify characteristics that appear aligned
     with the conference.

7. Why_This_Paper_May_Fit_This_Conference
   - Give a concise evidence-based explanation of why this paper
     appears suitable for this conference.

8. Observable_Conference_Profile
   - Create a concise profile of the type of research represented
     by this accepted paper.
   - Include research area, typical problem type, methodology,
     technical depth, evaluation style, and contribution type.

IMPORTANT:
The conference profile must describe characteristics OBSERVED in
this paper. Do not assume these characteristics are official
conference requirements unless the paper itself establishes that.

Return ONLY valid JSON.
"""

def analyze_paper(file_path, conference_name):

    with open(file_path, encoding="utf-8") as f:
        paper = f.read()

    response = client.chat.completions.create(
        model="qwen/qwen3-30b-a3b-instruct-2507",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"""
Conference Name:
{conference_name}

Research Paper:
{paper}
"""
            }
        ],
        temperature=0,
        max_tokens=6000
    )

    result = response.choices[0].message.content

    return result


input_folder = r"C:\Users\nagas\Desktop\IIT\Publishable_Papers_Parsed\TMLR_Parsed_Papers"
output_folder = r"C:\Users\nagas\Desktop\IIT\Publishable_Results_JSON\TMLR"

conference_name = "TMLR"

os.makedirs(output_folder, exist_ok=True)


for filename in os.listdir(input_folder):

    if filename.endswith(".md"):

        input_file = os.path.join(input_folder, filename)

        print(f"\nAnalyzing: {filename}")
        print(f"Conference: {conference_name}")

        result = analyze_paper(
            input_file,
            conference_name
        )

        output_file = os.path.join(
            output_folder,
            filename.replace(".md", ".json")
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"Saved: {output_file}")