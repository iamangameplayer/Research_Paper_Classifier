# Research Paper Classifier

An AI-powered research paper evaluation system that analyzes research papers, assesses their publishability based on research-quality criteria, and identifies conferences whose observed research profiles align with the paper.

The system uses Large Language Models (LLMs) and reference datasets of previously evaluated research papers to provide evidence-based assessments.

## Overview

Evaluating a research paper requires examining several aspects beyond its topic or writing quality. Research novelty, methodology, experimental validation, reproducibility, and contribution all play an important role.

This project aims to automate part of that evaluation process using an LLM-based approach.

It follows a reference-based evaluation strategy, comparing new research papers against patterns identified from two groups:

- **Publishable Papers:** Research papers used to identify characteristics associated with stronger research quality.
- **Non-Publishable Papers:** Research papers used to identify recurring weaknesses and limitations.

Based on these  patterns, the system evaluates a new paper and classifies it as either `Publishable` or `Non-Publishable`.

If classified as Publishable, the system performs an additional conference-alignment analysis to identify conferences whose observed research characteristics most closely match the paper.

## Key Features

- **PDF Parsing:** Converts research papers into structured Markdown content using LlamaParse.
- **Research Quality Evaluation:** Evaluates papers across 15 research-quality criteria.
- **Publishability Classification:** Compares new papers against reference patterns from publishable and non-publishable research.
- **Evidence-Based Scoring:** Assigns scores from 0 to 5 for each evaluation criterion, supported by evidence and explanations.
- **Conference Profiling:** Extracts recurring research characteristics from papers belonging to different conferences.
- **Conference Alignment:** Compares publishable papers against conference profiles and identifies matching characteristics.
- **Structured JSON Output:** Generates machine-readable JSON results for further analysis and evaluation.

## System Architecture

The project follows a multi-stage evaluation workflow:

1. **PDF Parsing:** Research papers are converted into Markdown using LlamaParse.
2. **Individual Paper Analysis:** Papers are evaluated using an LLM against 15 research-quality criteria.
3. **Reference Dataset Creation:** Analyses are organized into publishable and non-publishable groups.
4. **Comparative Analysis:** The two groups are compared to identify distinguishing research characteristics.
5. **Conference Profiling:** Accepted research papers are analyzed to generate conference-specific research profiles.
6. **New Paper Evaluation:** A new research paper is evaluated against the reference datasets.
7. **Conference Alignment:** If classified as Publishable, the paper is compared against available conference profiles.

## Research Evaluation Criteria

Each paper is evaluated using the following 15 criteria:

| No. | Evaluation Criterion |
|---|---|
| 1 | Research Problem |
| 2 | Research Gap |
| 3 | Novelty |
| 4 | Objectives |
| 5 | Literature Review |
| 6 | Methodology Rigor |
| 7 | Dataset Quality |
| 8 | Experimental Validation |
| 9 | Baseline Comparison |
| 10 | Evaluation Metrics |
| 11 | Results Quality |
| 12 | Statistical Validation |
| 13 | Reproducibility |
| 14 | Limitations |
| 15 | Overall Research Contribution |

Each criterion receives a score between 0 and 5.

| Score | Interpretation |
|---|---|
| 0 | Completely Absent |
| 1 | Very Weak |
| 2 | Weak |
| 3 | Adequate |
| 4 | Strong |
| 5 | Very Strong |

The system also provides supporting evidence and explanations for individual scores.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenRouter API | LLM API integration |
| Qwen3-30B-A3B-Instruct | Research paper evaluation and analysis |
| LlamaParse / LlamaCloud | PDF parsing and Markdown extraction |
| JSON | Reference datasets and structured evaluation outputs |
| python-dotenv | Environment variable management |

## Project Structure

```text
Research_Paper_Classifier/
│
├── Model.py
│
├── PDF_Parsing.py
│
├── Conference_Profiles.py
├── Conference_Profiles.json
│
├── Comparing_Evaluation_between_Conferences.py
├── Comparing_Evaluation_between_pub_nonpub.py
│
├── Publishability_Comparison.json
│
├── .gitignore
├── LICENSE
└── README.md
```

### Core Files

| File | Description |
|---|---|
| `PDF_Parsing.py` | Parses research paper PDFs into Markdown using LlamaParse. |
| `Model.py` | Evaluates new research papers and performs publishability classification and conference alignment. |
| `Conference_Profiles.py` | Analyzes conference papers and generates conference research profiles. |
| `Comparing_Evaluation_between_pub_nonpub.py` | Compares publishable and non-publishable paper analyses to identify distinguishing patterns. |
| `Comparing_Evaluation_between_Conferences.py` | Identifies common and distinctive characteristics across conference profiles. |
| `Conference_Profiles.json` | Stores generated conference research profiles. |
| `Publishability_Comparison.json` | Stores comparative findings between publishable and non-publishable papers. |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/iamangameplayer/Research_Paper_Classifier.git
```

Navigate into the project directory:

```bash
cd Research_Paper_Classifier
```

### 2. Create a Virtual Environment

```bash
python -m venv myvirenv
```

Activate it on Windows:

```powershell
.\myvirenv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install openai python-dotenv llama-cloud
```

### 4. Configure API Keys

Create a `.env` file in the project root directory.

Add your API credentials:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
LLAMA_PARSER_API_KEY=your_llamacloud_api_key
```

**Important:** Never upload your `.env` file or expose API credentials publicly.

### 5. Configure Project Paths

Some scripts currently use absolute Windows file paths.

Before running them, update the input and output directory paths inside the Python files to match your local project structure.

You will also need the appropriate PDF and reference datasets for the analysis stages.

## Execution

The individual scripts are currently designed as separate processing stages rather than a single command-line application.

Run the scripts according to the workflow:

```bash
python PDF_Parsing.py
```

```bash
python Conference_Profiles.py
```

```bash
python Comparing_Evaluation_between_pub_nonpub.py
```

```bash
python Comparing_Evaluation_between_Conferences.py
```

```bash
python Model.py
```

Make sure the required input files, reference JSON datasets, API keys, and directory paths are configured before executing each script.

## Output

The system generates structured JSON containing:

- Individual research criterion scores.
- Supporting evidence from the research paper.
- Explanations for each criterion.
- Final publishability classification.
- Overall evaluation reasoning.
- Strongest research strengths and weaknesses.
- Confidence level.
- Conference alignment assessments, when applicable.
- Recommendations for research improvement.

Conference alignment is categorized into:

- Strong Alignment
- Moderate Alignment
- Weak Alignment

## Limitations

- The reference dataset is relatively small and may not be generalized to other academic areas.
- Conference profiles describe observed characteristics of the supplied papers for the particular conference, not the  official conference requirements.
- LLM-generated evaluations may contain errors or overlook relevant information.
- Results depend on the quality of PDF extraction and the supplied reference data.
- A Publishable classification does not guarantee acceptance by a journal or conference.

This is a personal research paper classification workflow built to understand the working of LLM based parsing and classification based on various criteria.

## Future Improvements

- Develop  automated pipeline for all processing stages.
- Replace hardcoded paths with configurable project directories.
- Expand the reference dataset with more research papers and conferences.
- Introduce a user-friendly interface for uploading and evaluating papers.
- Add more comprehensive benchmarking and performance evaluation.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the `LICENSE` file for details.

## Repository

GitHub: https://github.com/iamangameplayer/Research_Paper_Classifier
