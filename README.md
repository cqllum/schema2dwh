<img src="https://i.imgur.com/ISXNkvD.png">

#### ⚠️ Important Note!
##### `schema2dwh` is powered by AI - Google's Gemini - Please make sure to check all code outputs before enrolling this to production. Please also be aware that processing via this script will utilise the Gemini API where data is processed by Google.


# ⚙️ schema2dwh [AI Powered DB Schema to DWH Schema Creation Script]
`schema2dwh` is an open-source framework designed to simplify and automatically produce a data model based on your database using its information schema, leverage AI, and a few questions about your inputs, it will quickly produce you a SQL DDL file, ready for creating the skeleton behind your newly built data warehouse.

## Features
- Interactively gather necessary inputs from the user
- Use Google Generative AI to generate a STAR/SNOWFLAKE schema
- Supports various database software (MySQL, SQL Server, PostgreSQL, etc.)
- Outputs SQL DDL statements compatible with the specified database software
- adds comments to all columns for reference to your database users
- Saves the generated schema to a specified output file

## Preview:
Please see below for an example of how it works.

#### Input (Running the script using `my_schema.csv`:

<img src="https://i.imgur.com/0JCzTSy.png">

#### Output DDL (`output_schema.sql`:

<img src="https://i.imgur.com/VqNapJ3.png">

## Prerequisites
- Python 3.x
- Google Generative AI Python package (`google-generativeai`)
- Google Generative AI API key - https://aistudio.google.com/app/apikey

## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/cqllum/schema2dwh.git
    cd schema2dwh
    ```

2. **Install the required packages:**
    ```sh
    pip install google-generativeai
    ```

3. **Set up your Google Generative AI API key:**
    Replace the placeholder `your-api-key` in the script with your actual Google Generative AI API key.
    Generate a key here: https://aistudio.google.com/app/apikey


4. **Replace example input schema file (my_schema.csv):**
    Please note, in order for this to be as accurate as possible, you will need to fetch the information schema from your database.
    In most cases, it is as simple as `SELECT * FROM information_schema.columns` - Otherwise, attend your database softwares documentation.

## Usage

1. **Run the script:**
    ```sh
    python schema2dwh.py
    ```

2. **Follow the prompts:**
    The script will prompt you for the following information:
    - Database software (e.g., MySQL, SQL Server, PostgreSQL)
    - Database/schema name
    - Industry related to your database (e.g., ecommerce, construction, insurance)
    - Naming convention for tables/columns (e.g., snake_case, PascalCase, camelCase)
    - File path to the information schema in CSV format
    - Important data points for reporting

3. **Output:**
    The script will generate the DDL SQL statements and save them to `output_schema.sql`. If the schema cannot be generated, it will prompt you to provide a proper information schema.


## Script Structure
- `configure_genai(api_key)`: Configures the Generative AI model with the provided API key.
- `create_model()`: Creates and configures the Generative AI model with the specified settings.
- `start_chat_session(model)`: Starts a chat session with the model using predefined instructions.
- `gather_user_input()`: Gathers necessary inputs from the user interactively.
- `format_response(db_software, db_name, industry, case_type, input_schema, additional_value)`: Formats the user inputs into a response for the chat session.
- `save_schema_to_file(output_file, schema_output)`: Saves the generated schema output to the specified file.
- `main()`: The main function that drives the script.
