from llama_cloud import LlamaCloud
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

parser = LlamaCloud(
    api_key= os.getenv("LLAMA_PARSER_API_KEY")
)

input_papers = Path(r"C:\Users\nagas\Desktop\IIT\Papers")
output_papers = Path(r"C:\Users\nagas\Desktop\IIT\Test_Parsed_Papers")


output_papers.mkdir(exist_ok=True)

for i in input_papers.glob("*.pdf"):
    print(f"Currently at this pdf {i.name}")
    paper = parser.files.create(
        file = str(i),
        purpose = "parse"
    )
    parsed_result = parser.parsing.parse(
        file_id=paper.id,
        tier="agentic",
        version="latest",
        expand=["markdown"]
    )

    output_path = output_papers / f"{i.stem}.md"

    with open(output_path, "w", encoding="utf-8") as f:
        for j in parsed_result.markdown.pages:
            f.write(j.markdown)
            f.write("\n\n")
    print(f"Saved the file {output_path.name}")