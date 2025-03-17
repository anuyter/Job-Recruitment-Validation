import os
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
    asyncio.run(main())































































































'''import os
import asyncio
from dotenv import load_dotenv

# Add Azure OpenAI package


# Set to True to print the full response from OpenAI for each call
printFullResponse = False

async def main(): 
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Configure the Azure OpenAI client
        

        while True:
            # Pause the app to allow the user to enter the system prompt
            print("------------------\nPausing the app to allow you to change the system prompt.\nPress enter to continue...")
            input()

            # Read in system message and prompt for user message
            system_text = open(file="system.txt", encoding="utf8").read().strip()
            user_text = input("Enter user message, or 'quit' to exit: ")
            if user_text.lower() == 'quit' or system_text.lower() == 'quit':
                print('Exiting program...')
                break
            
            await call_openai_model(system_message = system_text, 
                                    user_message = user_text, 
                                    model=azure_oai_deployment, 
                                    client=client
                                    )

    except Exception as ex:
        print(ex)

async def call_openai_model(system_message, user_message, model, client):
    # Get response from Azure OpenAI
    


    if printFullResponse:
        print(response)

    print("Response:\n" + response.choices[0].message.content + "\n")

if __name__ == '__main__': 
    asyncio.run(main())'''
