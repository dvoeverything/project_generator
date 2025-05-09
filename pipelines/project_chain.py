
from src.services.parts_service import fetch_parts
from src.services.llm_service  import generate_project
from src.retrievers.standards  import get_standards   
from src.parsers.lesson_plan   import lesson_extractor
from src.prompts.template      import build_prompt    
from config.grade_rules        import GRADE_RULES

def run_pipeline(pdf_path: str, domain="AUTO"):
  
    lp_bytes = open(pdf_path, "rb").read()
    lesson   = lesson_extractor(lp_bytes)
    grade    = lesson["grade"]

    
    vars = dict(
        lesson_summary=lesson["summary"],
        standards     = get_standards(lesson["topics"]),
        grade         = grade,
        weeks         = lesson["weeks"],
        domain        = domain,
        grade_rules   = GRADE_RULES[str(grade)]
    )

  
    messages = [{"role": "user", "content": build_prompt(vars)}]
    project  = generate_project(messages, grade=grade)   

    return project
