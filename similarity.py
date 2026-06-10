def calculate_match_score(user_skills, job_skills, return_details=False):
    user_skills = set([s.lower().strip() for s in user_skills])
    job_skills = set([s.lower().strip() for s in job_skills])

    matched = list(user_skills & job_skills)
    missing = list(job_skills - user_skills)
    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    if return_details:
        return round(score, 2), {
            "Matched Skills": matched,
            "Missing Skills": missing
        }
    return round(score, 2)
