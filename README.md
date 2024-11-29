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

## Development Setup

For local development with remote access:

1. Install ngrok:
   ```bash
   # On Windows (using chocolatey)
   choco install ngrok
   
   # On macOS
   brew install ngrok
   ```

2. Start the Flask development server:
   ```bash
   flask run
   ```

3. In a separate terminal, start ngrok:
   ```bash
   ngrok http 5000
   ```

4. Access your application through the ngrok URL provided

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t bloom .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 bloom
   ```

## License

MIT License
