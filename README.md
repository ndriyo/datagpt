# datagpt

Datagpt is a project that connects to an SQL Server database and leverages language model providers such as OpenAI or Azure OpenAI for various tasks.

## Environment Variables

Before running the project, ensure you have set the following environment variables (commonly in a .env file):

- CONN_STR: Specifies the ODBC connection string for SQL Server. Example:
  Driver={ODBC Driver 18 for SQL Server};Server=YOUR_SERVER;Database=YOUR_DATABASE;Uid=YOUR_USERNAME;Pwd=YOUR_PASSWORD;

- LLM_PROVIDER: The language model provider to be used. Currently supported value is "openai".

- OPENAI_MODEL: The OpenAI model to be used (e.g., gpt-4o).

- OPENAI_API_KEY: Your API key for OpenAI.

- AZURE_OPENAI_ENDPOINT: The endpoint URL for Azure OpenAI. Example: "https://your-azure-openai-endpoint"

- AZURE_OPENAI_KEY: The API key for Azure OpenAI.

- AZURE_OPENAI_DEPLOYMENT: The deployment name for Azure OpenAI (e.g., gpt-4o).

- AZURE_OPENAI_API_VERSION: The API version for Azure OpenAI (e.g., 2024-12-01-preview).

## Setup and Installation

1. Clone the repository.
2. Copy the provided .env example (or create a new .env file) and fill in the required values.
3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the application:

   ```sh
   python run.py
   ```

## Running with Docker

This project includes a Dockerfile for containerized deployment. To build and run the container:

1. Build the Docker image:

   ```sh
   docker build -t datagpt .
   ```

2. Run the container with environment variables:

   ```sh
   docker run --env-file .env datagpt
   ```

## Additional Notes

- Ensure that your environment variables are securely managed and not exposed publicly.
- The project may require additional configuration depending on your deployment environment.
