# Kaggle Gen AI Capstone Project - Project Pathfinder

## Introduction

This is my submission for Kaggle's Capstone Project as part of the [5 Day Gen AI Intensive Course with Google](https://www.kaggle.com/learn-guide/5-day-genai).

This project features a basic TUI chat interface that allows user to interact with an agent created with [Google ADK](https://google.github.io/adk-docs/).

These are the primary capabilities of the agent:

1. Generate travel itinerary.
2. Generate plans for achieving personal goals.
3. Save generated plans to either Notion or local Obsidian vault.

## Environment Setup

### 1. Prerequisites

- Make sure you have at least [Python 3.10](https://www.python.org/downloads/) installed on your environment. This is important as [Google ADK for Python v1.19.0](https://github.com/google/adk-python/releases/tag/v1.19.0) requires Python 3.10 or higher to function properly.

### 2. Clone repo

Download the project to your working directory, or you can just use `git clone`.

```
git clone https://github.com/dwardTheNerd/KaggleGenAICapstoneProject.git
```

### 3. Setting up a Virtual Environment

#### 1. Create virtual environment
Create a virtual environment in your working directory. If you do not have venv, you need to install it for the version of Python you are using.

```bash
python3 -m venv .venv
```

#### 2. Activate Virtual Environment

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows (Command Prompt)**:

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**:

```PowerShell
.venv\Scripts\Activate.ps1
```

#### 3. Installing Dependencies

Choose either options:

**Option A: Using pip and requirements.txt:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
  ```

**Option B: Using pip and Editable Install:**

```bash
pip install --upgrade pip
pip install -e .
```

## Obtaining API Keys

### Google API Key

Obtain API key from [Google AI Studio](https://aistudio.google.com/)

#### 1. Go to AI Studio

![Go to Google AI Studio](docs/images/Google_AI_Studio_API_keys_1.png)

#### 2. Create API Key

![Click Create API Key](docs/images/Google_AI_Studio_API_keys_2.png)

![Create new key](docs/images/Google_AI_Studio_API_keys_3.png)

#### 3. Copy API Key

![Copy key](docs/images/Google_AI_Studio_API_keys_4.png)

### Notion Token ###

[Notion](https://www.notion.com) is an all-in-one productivity and workspace app that combines note-taking, task management, project planning, and AI-powered tools into a single customizable platform.

A Notion API key or token is required for the agent to create new Notion pages. Go to (https://www.notion.so/profile/integrations) to set up a new **internal** integration.

#### 1. Create internal integration

![Create internal integration](docs/images/Notion_create_integration_1.png)

![Fill in internal integration details](docs/images/Notion_create_integration_2.png)

#### 2. Copy secret from the integration's settings page

![Copy secret](docs/images/Notion_copy_secret.png)

#### 3. Configure Capabilities

![Configure capabilities](docs/images/Notion_set_capabilities.png)

#### 4. Configure Access

![Configure capabilities](docs/images/Notion_set_access_1.png)

![Configure capabilities](docs/images/Notion_set_access_2.png)

### Obsidian API Key ###

[Obsidian](https://obsidian.md/) is a popular note-taking and personal knowledge base tool.

For the agent to create notes in your local Obsidian vault, you need to install and run the [Obsidian REST API community plugin](https://github.com/coddingtonbear/obsidian-local-rest-api).

#### 1. Install REST API community plugin in Obsidian

![Install REST API plugin](docs/images/Obsidian_install_REST_plugin.png)

#### 2. Enable REST API community plugin

![Enable plugin](docs/images/Obsidian_enable_REST_plugin.png)

#### 4. Access REST API settings

![Access REST API settings](docs/images/Obsidian_REST_settings.png)

#### 5. Copy API Key and port number

![Copy REST API key and port](docs/images/Obsidian_REST_copy_key.png)

## Configuration

1. In pathfinder folder, rename `.env.example` to `.env`
2. Open `.env`
3. Provide GOOGLE_APY_KEY:

  ```
  GOOGLE_API_KEY=PROVIDE GOOGLE_API_KEY HERE
  ```

4. Provide NOTION_TOKEN:

  ```
  NOTION_TOKEN=PROVIDE NOTION_TOKEN HERE
  ```

5. Provide OBSIDIAN_API_KEY, OBSIDIAN_HOST and OBSIDIAN_PORT:

  ```
  OBSIDIAN_API_KEY=PROVIDE OBSIDIAN_API_KEY HERE
  OBSIDIAN_HOST=PROVIDE OBSIDIAN_HOST
  OBSIDIAN_PORT=PROVIDE OBSIDIAN_PORT
  ```

  `OBSIDIAN_HOST` should be where you are running Obsidian.

  6. Save changes

## Running the Project

To run the project, make sure you are in the **KaggleGenAICapstoneProject** folder and not in the pathfinder folder, then run the following:

```bash
python3 -m pathfinder.main
```

## Debugging

The TUI application and Google ADK utilize Python's logging package for collecting logs. Logs are configured to output to `.log` files under the logs folder.

For more visibility into the agents' operations, you can change the logging_level in `config.json`.

Change logging_level to *DEBUG*:

```json
{
  "logging_level": "DEBUG"
}
```