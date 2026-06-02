import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# ─── Companies ───
def create_company(company_data):
    return supabase.table("companies").insert(company_data).execute()

def get_company_by_name(name):
    result = supabase.table("companies").select("*").eq("name", name).execute()
    return result.data[0] if result.data else None

def get_company_by_id(company_id):
    result = supabase.table("companies").select("*").eq("id", company_id).execute()
    return result.data[0] if result.data else None

# ─── Users ───
def add_user(user_data):
    return supabase.table("users").insert(user_data).execute()

def get_user_by_email(email):
    result = supabase.table("users").select("*").eq("email", email).execute()
    return result.data[0] if result.data else None

def get_users_by_company(company_id):
    result = supabase.table("users").select("*").eq("company_id", company_id).execute()
    return result.data

# ─── Jobs ───
def add_job(job_data):
    return supabase.table("jobs").insert(job_data).execute()

def get_jobs_by_user(user_id):
    result = supabase.table("jobs").select("*").eq("user_id", user_id).execute()
    return result.data

def get_jobs_by_company(company_id):
    result = supabase.table("jobs").select("*").eq("company_id", company_id).execute()
    return result.data

def get_job_by_id(job_id):
    result = supabase.table("jobs").select("*").eq("id", job_id).execute()
    return result.data[0] if result.data else None

# ─── Candidates ───
def add_candidate(candidate_data):
    return supabase.table("candidates").insert(candidate_data).execute()

def get_candidates_by_user(user_id):
    result = supabase.table("candidates").select("*").eq("user_id", user_id).execute()
    return result.data

def get_candidates_by_company(company_id):
    result = supabase.table("candidates").select("*").eq("company_id", company_id).execute()
    return result.data

def get_candidate_by_id(candidate_id):
    result = supabase.table("candidates").select("*").eq("id", candidate_id).execute()
    return result.data[0] if result.data else None

def update_candidate(candidate_id, update_data):
    return supabase.table("candidates").update(update_data).eq("id", candidate_id).execute()

def delete_candidate(candidate_id, user_id):
    result = supabase.table("candidates").delete().eq("id", candidate_id).eq("user_id", user_id).execute()
    return result.data

# ─── Applications ───
def add_application(app_data):
    return supabase.table("applications").insert(app_data).execute()

def get_applications_by_company(company_id):
    result = supabase.table("applications").select("*, candidates!inner(company_id)").eq("candidates.company_id", company_id).execute()
    return result.data

# ─── Analysis Results ───
def add_analysis_result(result_data):
    return supabase.table("analysis_results").insert(result_data).execute()