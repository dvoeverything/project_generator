from supabase import create_client
import os

sb = create_client(os.getenv("SUPABASE_URL"),
                   os.getenv("SUPABASE_SERVICE_KEY"))

def fetch_parts(grade: int, domain: str = "AUTO"):
    q = (sb.table("parts")
           .select("*")
           .lte("grade_min", grade)
           .gte("grade_max", grade))
    if domain != "AUTO":
        q = q.eq("domain", domain)
    return q.execute().data
