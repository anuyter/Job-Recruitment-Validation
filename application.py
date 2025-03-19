import os
import asyncio
from dotenv import load_dotenv
import openai
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
database_url = os.getenv("DATABASE_URL")

# OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = azure_oai_endpoint
openai.api_key = azure_oai_key
openai.api_version = "2023-12-01-preview"

# SQLAlchemy Database Configuration
engine = create_engine(database_url)

def validate_candidate_identity(candidate_name, email):
    """
    Validates candidate identity using database.
    """
    try:
        query = text("SELECT * FROM candidates WHERE name = :name AND email = :email")
        with engine.connect() as connection:
            result = connection.execute(query, {"name": candidate_name, "email": email})
            return result.fetchone() is not None
    except Exception as e:
        print(f"Database error: {e}")
        return False

async def call_openai_model(thread_name, system_message, user_message):
    """
    Calls OpenAI API asynchronously for a given thread (job section).
    """
    try:
        # Perform database validation if applicable
        if "Validate candidate contact details" in user_message:
            candidate_name = "John Doe"
            email = "john.doe@example.com"
            is_valid = validate_candidate_identity(candidate_name, email)
            if is_valid:
                print(f"{thread_name}: ✅ Candidate validated from database.")
            else:
                print(f"{thread_name}: ❌ Candidate not found in database.")
        
        # Call Azure OpenAI
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model=azure_oai_deployment,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        result = response["choices"][0]["message"]["content"]
        print(f"{thread_name} Response:\n{result}\n")
        return result
    except Exception as e:
        print(f"Error in {thread_name}: {e}")
        return None

async def main():
    try:
        # Read System Message
        system_text = open(file="system.txt", encoding="utf8").read().strip()

        # Define tasks for different validation sections
        tasks = [
            call_openai_model("1. Company Philosophy", system_text,
                               "Explain the vision, mission, and goals of a recruiting company."),
            
            call_openai_model("2. Candidate Contact Details", system_text,
                               "Validate candidate contact details including name, email, and phone number."),
            
            call_openai_model("3. Job Title Selection", system_text,
                               "Validate and process job title selection from AI and Cybersecurity to NLP experts."),
            
            call_openai_model("4. Job Description", system_text,
                               "Provide details on AI, Cybersecurity, Data Science, NLP job descriptions."),
            
            call_openai_model("5. Job Experience", system_text,
                               "Validate and store job experience details such as title, company, duration, and reason for leaving."),
            
            call_openai_model("6. Qualifications", system_text,
                               "Check educational qualifications and validate certifications."),
            
            call_openai_model("7. Personal Details", system_text,
                               "Process bio, date of birth, residence, and means of identification."),
            
            call_openai_model("8. Gender Selection", system_text,
                               "Validate and store gender information."),
            
            call_openai_model("9. Inclusiveness/Fairness", system_text,
                               "Check if the candidate belongs to underrepresented groups or specific regions."),
            
            call_openai_model("10. Medical Status", system_text,
                               "Verify medical reports and eligibility based on health requirements."),
            
            call_openai_model("11. Hobbies & Interests", system_text,
                               "Store hobbies and interests for cultural fit assessment."),
            
            call_openai_model("12. References/Recommendations", system_text,
                               "Validate candidate references and recommendations."),
            
            call_openai_model("13. Resume & Cover Letter Upload", system_text,
                               "Process uploaded resume, cover letter, and certificates."),
        ]

        # Run tasks concurrently
        results = await asyncio.gather(*tasks)
        print("\n✅ All threads completed execution.")
    
    except Exception as ex:
        print("Error in main execution:", ex)

if __name__ == '__main__':
    asyncio.run(main())


















































































'''import os
import asyncio
from dotenv import load_dotenv
import openai  # Install via `pip install openai`

# Set to True to print full response from OpenAI
printFullResponse = False

# Load environment variables
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

# OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = azure_oai_endpoint
openai.api_key = azure_oai_key
openai.api_version = "2023-12-01-preview"  # Update if needed


async def call_openai_model(thread_name, system_message, user_message):
    """
    Calls OpenAI API asynchronously for a given thread (job section).
    """
    try:
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model=azure_oai_deployment,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        result = response["choices"][0]["message"]["content"]
        print(f"{thread_name} Response:\n{result}\n")
        return result
    except Exception as e:
        print(f"Error in {thread_name}: {e}")
        return None


async def main():
    try:
        # Read System Message (General Guidelines for AI Model)
        system_text = open(file="system.txt", encoding="utf8").read().strip()

        # Define 13 sections as tasks
        tasks = [
            call_openai_model("1. Company Philosophy", system_text,
                              "Explain the vision, mission, and goals of a recruiting company."),
            
            call_openai_model("2. Candidate Contact Details", system_text,
                              "Validate candidate contact details including name, email, and phone number."),
            
            call_openai_model("3. Job Title Selection", system_text,
                              "Validate and process job title selection from AI and Cybersecurity to NLP experts."),
            
            call_openai_model("4. Job Description", system_text,
                              "Provide details on AI, Cybersecurity, Data Science, NLP job descriptions."),
            
            call_openai_model("5. Job Experience", system_text,
                              "Validate and store job experience details such as title, company, duration, and reason for leaving."),
            
            call_openai_model("6. Qualifications", system_text,
                              "Check educational qualifications and validate certifications."),
            
            call_openai_model("7. Personal Details", system_text,
                              "Process bio, date of birth, residence, and means of identification."),
            
            call_openai_model("8. Gender Selection", system_text,
                              "Validate and store gender information."),
            
            call_openai_model("9. Inclusiveness/Fairness", system_text,
                              "Check if the candidate belongs to underrepresented groups or specific regions."),
            
            call_openai_model("10. Medical Status", system_text,
                              "Verify medical reports and eligibility based on health requirements."),
            
            call_openai_model("11. Hobbies & Interests", system_text,
                              "Store hobbies and interests for cultural fit assessment."),
            
            call_openai_model("12. References/Recommendations", system_text,
                              "Validate candidate references and recommendations."),
            
            call_openai_model("13. Resume & Cover Letter Upload", system_text,
                              "Process uploaded resume, cover letter, and certificates."),
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Optional: Store or process results
        print("\n✅ All threads completed execution.")
    
    except Exception as ex:
        print("Error in main execution:", ex)


if __name__ == '__main__':
    asyncio.run(main())'''































































































