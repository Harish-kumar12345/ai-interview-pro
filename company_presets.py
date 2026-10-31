from typing import Any

COMPANY_PROFILES = {
    "General / Standard": {
        "description": "Standard industry benchmark questions evaluating core technical competence.",
        "prompt_context": "Follow standard professional interview standards balancing foundational and practical knowledge."
    },
    "Google": {
        "description": "Emphasis on high-scale data structures, algorithmic complexity (Big-O), distributed systems, and clean idiomatic code.",
        "prompt_context": "Evaluate like Google interviewers: focus heavily on scalability, algorithmic optimization, edge cases, trade-offs, and clean architectural design."
    },
    "Amazon": {
        "description": "Heavy focus on Amazon Leadership Principles (Customer Obsession, Ownership, Bias for Action), scalable system design, and practical trade-offs.",
        "prompt_context": "Incorporate Amazon Leadership Principles (Customer Obsession, Deep Dive, Deliver Results). Frame behavioral and system design questions around real customer impacts, metrics, and scalable microservices."
    },
    "Microsoft": {
        "description": "Strong emphasis on modular object-oriented design, robust edge-case handling, cloud services (Azure patterns), and maintainable architecture.",
        "prompt_context": "Focus on robust software engineering practices, design patterns, testing strategies, clarity of communication, and cloud-native resilience."
    },
    "Meta (Facebook)": {
        "description": "Fast-paced problem solving, product architecture, concurrency, and rapid iteration mindset.",
        "prompt_context": "Emphasize product architecture, moving fast, high concurrency, caching layers, and clear end-to-end user experience."
    },
    "TCS / Infosys / Wipro": {
        "description": "Core computer science fundamentals: OOP, DBMS, SQL queries, OS concepts, and structured logical thinking.",
        "prompt_context": "Focus on solid fundamentals: OOPs concepts, normalization, SQL joins, basic DSA, problem-solving aptitude, and clear verbal communication."
    },
    "High-Growth Startup": {
        "description": "Hands-on practicality, shipping MVPs rapidly, full-stack debugging, REST API design, and startup agility.",
        "prompt_context": "Focus on practical execution: pragmatism over over-engineering, end-to-end debugging, modern frameworks, database performance, and cross-functional agility."
    }
}


def get_company_prompt_note(company_name: str) -> str:
    profile = COMPANY_PROFILES.get(company_name)
    if not profile or company_name == "General / Standard":
        return ""
    return f"\nTarget Company Context ({company_name}): {profile['prompt_context']}\n"

