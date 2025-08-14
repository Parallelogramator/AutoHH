from collections import Counter
from typing import List, Dict, Set

def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b: return 0.0
    return len(a & b) / len(a | b) if len(a | b) > 0 else 0.0

def compute_score(profile_skills: List[str], vacancy_skills: List[str], must_have: List[str] = []) -> Dict:
    profile_set = set(s.lower().strip() for s in profile_skills)
    vacancy_set = set(s.lower().strip() for s in vacancy_skills)
    must_have_set = set(s.lower().strip() for s in must_have)

    coverage = jaccard(profile_set, vacancy_set)

    gaps_in_must_have = [s for s in must_have_set if s not in profile_set]

    # Штраф за каждый отсутствующий обязательный навык
    penalty = 0.2 * len(gaps_in_must_have)

    score = max(0.0, min(1.0, coverage - penalty))

    return {"score": round(score, 3), "gaps": gaps_in_must_have}
