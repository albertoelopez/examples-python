# Restack AI SDK - FastAPI + Gemini Generate Content Example

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Google AI Studio](https://aistudio.google.com) account with API key

## Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name studio -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/engine:main
   ```

2. Open the web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/examples/fastapi_gemini_feedback
   ```

4. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

5. Set `GEMINI_API_KEY` as an environment variable from [Google AI Studio](https://aistudio.google.com)

   ```bash
   export GEMINI_API_KEY=<your-api-key>
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, run flask app:

   ```bash
   poetry run app
   ```

8. POST to `http://127.0.0.1:5000/api/schedule` with the following JSON body:

   ```json
   {
     "user_content": "Tell me a story"
   }
   ```

   This will schedule the `GeminiGenerateWorkflow` and print the result.

9. POST to `http://127.0.0.1:5000/api/event/feedback` with the following JSON body:

   ```json
   {
     "feedback": "The story is too long"
   }
   ```

   This will send an event to the `GeminiGenerateWorkflow` to update the workflow state with the feedback.

10. POST to `http://127.0.0.1:5000/api/event/end` to end the workflow.

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
  - `app.py`: Flask app to schedule and run workflows