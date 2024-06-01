
import google.generativeai as genai

# API Token gathered from Gemini 
# https://aistudio.google.com/app/apikey
api_key = 'your-api-key'

# Define where you want to output the schema to
output_file = 'output_schema.sql'


# Prepare gemini genAI
def configure_genai(api_key):
    """Configure the Generative AI model."""
    genai.configure(api_key=api_key)

# Prepare the models settings
def create_model():
    """Create and configure the generative AI model."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )
    return model

# Train the model with some history and context
def start_chat_session(model):
    """Start a chat session with the model."""
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are a chatbot whose focus is to prepare database BI fct/dim tables for better processing of business data which will be consumed by BI/Data analysts.",
                    "The schema you produce will be developed and made as production tables by a proper data engineer, your reply IS important.",
                    "You must respond with an error if the user does not supply a proper industry.",
                    "You must simply only answer once the user has given a response relating to an industry.",
                    "If the user does not give you a database schema to create the tables in, use reporting",
                    "The output schema you produce must be only made up of what the user supplies.",
                    "The user will supply you with the information schema which will be supplied as JSON format for all columns in the database.",
                    "You will respond with the STAR/SNOWFLAKE schema including CREATE TABLE statements",
                    "The schema you respond with should only contain columns seen in the information schema supplied",
                    "You must not produce a schema that has columns not seen in the schema file, or made up from nothing, other than for primary keys.",
                    "If you cannot produce a conclusion, or if the file doesn't look like an information schema, return false.",
                    "The user will also supply you with the database software they use. Only produce outputs compatible with their software.",
                    "The user will supply you with the case they want to generate the table/column names in",
                    "The user will supply you a CSV file of their information schema, your job is to work out the value based on common industry schema setups and identify where the value lies.",
                    "The response you give should be in the form of a DDL SQL file that will be used by a python script to save to a tangible file. The DDL should be accurate to the Database Software",
                    "The user will supply you with a database name, include a USE Statement and a Create database if not exists statement relating to their database software.",
                    "Do not include embed ```sql in the response",
                    "Include comments on all columns given in the DDL to be added as a COMMENT on the actual columns upon creation.",
                    "You must not answer anything else.",
                ],
            },
        ]
    )
    return chat_session

# Gather data needed for the chatbot
def gather_user_input():
    """Gather necessary inputs from the user."""
    db_software = input("What database software do you use? (MySQL, SQL Server, Postgres, etc)? \n> ")
    db_name = input("\nWhich database/schema would you like to create your schema in? (default reporting) \n> ")
    industry = input("\nWhat industry is your database related to? (ecommerce, construction, insurance, etc) \n> ")
    case_type = input("\nHow would you like your tables/columns named? (Snake case, pascal case, camel case, etc)? \n> ")
    information_schema_file = input("\nWhere is the information schema stored (csv)? Please supply a file path \n> ")

    try:
        input_schema = open(information_schema_file, "r").read()
    except:
        information_schema_file = input("\nUh oh, that didn't work - Where is the information schema stored (csv)? Please supply a file path \n> ")
        input_schema = open(information_schema_file, "r").read()

    additional_value = input("\nIn your own words, where does the value lie in your data/what tables are important for reporting? \n> ")

    return db_software, db_name, industry, case_type, input_schema, additional_value


# Structure the resposne that will be sent back to the chatbot
def format_response(db_software, db_name, industry, case_type, input_schema, additional_value):
    """Format the response to send to the chat session."""
    response = f'''
    My database software used is:
    {db_software}

    The database I want to create the reporting schema in is:
    {db_name}

    My database is based on the following industry: (ecommerce, construction, insurance, etc) 
    {industry}.

    I want my tables named in the following case:
    {case_type}

    In my opinion, to assist you in your decision, I think the most important data points are related to:
    {additional_value}

    My information schema in CSV format is below:
    {input_schema}
    '''
    return response

# Save the schema gained from the AI bot to a file
def save_schema_to_file(output_file, schema_output):
    """Save the schema output to a file."""
    with open(output_file, "w") as out_file:
        out_file.write(schema_output.replace("```sql", "").replace("```", ""))

# Main script
def main():

    print(f'''
    #######################################################################
    #            _                          ___     _          _          #
    #           | |                        |__ \   | |        | |         #
    #   ___  ___| |__   ___ _ __ ___   __ _   ) |__| |_      _| |__       #
    #  / __|/ __| '_ \ / _ \ '_ ` _ \ / _` | / // _` \ \ /\ / / '_ \      #
    #  \__ \ (__| | | |  __/ | | | | | (_| |/ /| (_| |\ V  V /| | | |     #
    #  |___/\___|_| |_|\___|_| |_| |_|\__,_|____\__,_| \_/\_/ |_| |_|     #
    #                                                                     #                                              
    #######################################################################
    ~ Generate a Data Warehouse Schema from your databases schema with AI
    #######################################################################
        
    Answer a few questions and your reporting schema will be dumped to:
    {output_file}
    ''')

    db_software, db_name, industry, case_type, input_schema, additional_value = gather_user_input()
    configure_genai(api_key)
    model = create_model()
    chat_session = start_chat_session(model)
    response = format_response(db_software, db_name, industry, case_type, input_schema, additional_value)
    
    schema_output = chat_session.send_message(response)

    if schema_output.text.strip() == 'false':
        print("Could not determine fact/dim tables successfully, please provide a proper information schema.")
    else:
        print(f"Dumped file to {output_file}")
        save_schema_to_file(output_file, schema_output.text)

if __name__ == "__main__":
    main()
