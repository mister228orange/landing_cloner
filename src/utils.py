import os



def create_server(folder_path, html_content):
    """Create the Flask app files (app.py, requirements.txt, templates)."""
    # Create app.py
    with open(os.path.join(folder_path, "app.py"), "w") as f:
        f.write(open("server.template", 'r').read())
    
    # Create requirements.txt
    with open(os.path.join(folder_path, "requirements.txt"), "w") as f:
        f.write("flask\n")
    templates_dir = os.path.join(folder_path, "templates")
    os.makedirs(templates_dir, exist_ok=True)
    
    with open(os.path.join(templates_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return True


def create_dockerfile(folder_path):
    """Create a Dockerfile for the Flask app."""
    dockerfile_content = '''FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
'''
    
    with open(os.path.join(folder_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)



def get_folder_name(url):
    """Generate a safe folder name from URL."""
    # Remove protocol and special characters
    clean_name = url.replace("https://", "").replace("http://", "")
    clean_name = clean_name.replace("/", "_").replace(".", "_")
    return f"{clean_name}_clone"
