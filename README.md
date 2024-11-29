# Bloom

Bloom is an intermediary server that interfaces between a sandboxed Python environment and a language model (LLM), facilitating software growth through command execution, error handling, and user interaction.

## Features

- Sandboxed Python environment for secure code execution
- Task management system
- File management and upload capabilities
- Web interface with mobile responsiveness
- Support for both local and cloud deployment

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///app.db
   ```
5. Initialize the database:
   ```bash
   flask db upgrade
   ```

## Running the Application

For local development:
```bash
flask run
```

For production deployment, refer to the deployment documentation.

## License

MIT License
