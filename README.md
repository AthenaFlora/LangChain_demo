# AI-Powered CV & Cover Letter Generator

This project uses AI to generate tailored CVs and cover letters based on your profile and job descriptions.

## Features

- Parse markdown-formatted profiles
- Process job descriptions (raw text or LinkedIn URLs)
- Generate customized CVs and cover letters
- Multiple tone options (original, precise, professional)
- Output in Markdown format

## Setup Options

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd cv-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Docker Setup

1. Build and run using Docker Compose:
```bash
docker compose up app
```

### Development with Dev Container

1. Install the following prerequisites:
   - Docker
   - Visual Studio Code
   - VS Code Remote - Containers extension

2. Open the project in VS Code:
```bash
code .
```

3. When prompted, click "Reopen in Container" or:
   - Press F1
   - Select "Dev Containers: Reopen in Container"

4. The container will build and set up the development environment with:
   - Python 3.9
   - Development tools (pylint, black, isort)
   - VS Code extensions for Python development
   - Auto-formatting on save
   - Debugging support

5. Create a `.env` file with your OpenAI API key as above.

## Usage

1. Create your profile:
   - Add a markdown file in `app/data/profiles/`
   - Use the example profile as a template

2. Run the generator:
```bash
python app/main.py
```

The generated CV and cover letter will be saved in `app/data/output/`.

## Configuration

Edit `app/config/settings.yaml` to customize:
- LLM settings (model, temperature)
- Tone styles
- Output formats
- File paths

## Project Structure

```
cv_agent/
├── app/
│   ├── core/
│   │   ├── profile_loader.py   # Profile parsing
│   │   ├── job_parser.py       # Job description processing
│   │   └── llm_interface.py    # LLM integration
│   ├── data/
│   │   ├── profiles/           # User profiles
│   │   ├── jobs/              # Saved job descriptions
│   │   └── output/            # Generated documents
│   └── main.py                # Main application
├── .devcontainer/            # Dev container configuration
│   ├── Dockerfile           # Development Dockerfile
│   └── devcontainer.json    # VS Code dev container settings
├── Dockerfile               # Production Dockerfile
├── docker-compose.yml       # Docker Compose configuration
├── config/
│   └── settings.yaml        # Configuration
└── requirements.txt         # Dependencies
```

## Requirements

- Python 3.8+
- OpenAI API key
- Required packages (see requirements.txt)
- Docker (for containerized usage)

## License

MIT License
