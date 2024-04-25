from fuzzywuzzy import fuzz
import json

# Define reference skills and experiences
reference_skills = ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"]
reference_experience = "Senior Software Engineer"

# Function to read content from a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the content from the JSON file
resume_data = read_json_file("/Users/sambucks/FuzzyWuzzyLogic/resume.json")

# Check if the 'resume' key exists in the resume_data dictionary
if "resume" in resume_data:
    # Extract skills and work experiences from the resume data
    resume = resume_data["resume"]
    skills_list = resume.get("skills", [])
    skills = " ".join(skills_list) if skills_list else ""  # Join skills into a single string if not empty
    experience = [exp["jobTitle"] for exp in resume.get("workExperience", [])]
else:
    print("The 'resume' key does not exist in the resume_data dictionary.")
    skills = ""
    experience = []

# Define function to calculate similarity scores
def calculate_similarity(reference, items):
    similarity_scores = {}
    if isinstance(reference, str):
        reference = [reference]
    for item in items:
        # Check if the item is a string before applying the lower() method
        if isinstance(item, str):
            similarity_scores[item] = fuzz.partial_ratio(reference[0].lower(), item.lower())
    return similarity_scores

# Calculate similarity scores for skills and experiences
if skills:
    skill_scores = calculate_similarity(reference_skills, skills.split())  # No need to split if skills is not empty
else:
    skill_scores = {}
experience_scores = calculate_similarity(reference_experience, experience)

# Filter and return matching experiences with high similarity scores
matching_experience = {exp: score for exp, score in experience_scores.items() if score >= 80}

# Output matching experiences
print("Matching Experiences:")
for exp, score in matching_experience.items():
    print(f"Experience: {exp}, Similarity Score: {score}")

# Output similarity scores for skills
print("Similarity Scores for Skills:")
for skill, score in skill_scores.items():
    print(f"Skill: {skill}, Similarity Score: {score}")