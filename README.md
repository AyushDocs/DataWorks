# LLM-based Automation Agent

This project is an automation agent that uses a Large Language Model (LLM) to execute operational and business tasks based on plain-English descriptions. The agent integrates with various tools, APIs, and file systems to automate routine tasks in the DataWorks Solutions CI pipeline.

## Project Overview

DataWorks Solutions processes large volumes of log files, reports, and code artifacts. To improve operational efficiency, routine tasks are being automated and integrated into their Continuous Integration (CI) pipeline. The task of this project is to build an automation agent that accepts plain-English task descriptions, parses them using an LLM, and carries out the necessary steps to complete the task, ensuring verifiable results.

### Tasks to Automate

- **Phase A**: Handles operational tasks such as processing data files, sorting records, counting specific entries in logs, etc.
- **Phase B**: Handles business tasks such as API calls, database queries, image manipulation, and more.
- **Security Considerations**: Ensures data access is restricted to only files within the `/data` directory and prevents data deletion.

## API Endpoints

### `POST /run?task=<task description>`

Executes a plain-English task. The agent will parse the task description, execute one or more steps, and produce the final output.

- **Success (200 OK)**: Task executed successfully.
- **Failure (400 Bad Request)**: Invalid task description.
- **Failure (500 Internal Server Error)**: Task execution failed due to an agent error.

#### Example Request

```bash
POST /run?task=Install+uv+and+run+datagen.py+with+${user.email}
```
