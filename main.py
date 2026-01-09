import os
import click
import subprocess
import sys


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Flask Clone CLI - Create Flask apps from web page clones using Docker."""
    pass


def get_folder_name(url):
    """Generate a safe folder name from URL."""
    # Remove protocol and special characters
    clean_name = url.replace("https://", "").replace("http://", "")
    clean_name = clean_name.replace("/", "_").replace(".", "_")
    return f"{clean_name}_clone"


def create_flask_app_structure(folder_path, html_content):
    """Create the Flask app files (app.py, requirements.txt, templates)."""
    # Create app.py
    with open(os.path.join(folder_path, "app.py"), "w") as f:
        f.write(open("server.template", 'r').read())
    
    # Create requirements.txt
    with open(os.path.join(folder_path, "requirements.txt"), "w") as f:
        f.write("flask\n")
    
    # Create templates directory and index.html
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


@cli.command()
@click.argument("url")
@click.option("--dockerfile", "-d", is_flag=True, help="Generate a Dockerfile.", default=False)
def clone(url, name, dockerfile):
    """Create a Flask app from a cloned web page."""
    
    # Validate URL
    if not url.startswith(("http://", "https://")):
        click.echo(click.style("Error: URL must start with http:// or https://", fg="red"))
        sys.exit(1)
    
    # Determine folder name
    folder_name = name if name else get_folder_name(url)
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Check if folder exists
    if os.path.exists(folder_path):
        click.echo(click.style(f"Error: Folder '{folder_name}' already exists.", fg="red"))
        sys.exit(1)
    
    click.echo(click.style(f"Creating Flask app from: {url}", fg="cyan"))
    click.echo(click.style(f"Project folder: {folder_path}", fg="cyan"))
    
    # Create folder
    try:
        os.makedirs(folder_path)
        click.echo(click.style("✓ Created project folder", fg="green"))
    except OSError as e:
        click.echo(click.style(f"Error creating folder: {e}", fg="red"))
        sys.exit(1)
    
    # Fetch HTML using Docker
    with click.progressbar(
        length=1, 
        label=click.style("Fetching page HTML with Docker", fg="yellow")
    ) as bar:
        html_content, error = run_docker_singlefile(url)
        bar.update(1)
    
    if error:
        click.echo(click.style(f"Error: {error}", fg="red"))
        # Clean up folder on error
        import shutil
        shutil.rmtree(folder_path)
        sys.exit(1)
    
    if not html_content or len(html_content.strip()) == 0:
        click.echo(click.style("Error: No HTML content received", fg="red"))
        import shutil
        shutil.rmtree(folder_path)
        sys.exit(1)
    
    # Create Flask app structure
    try:
        create_flask_app_structure(folder_path, html_content)
        click.echo(click.style("✓ Created Flask app structure", fg="green"))
    except Exception as e:
        click.echo(click.style(f"Error creating app structure: {e}", fg="red"))
        import shutil
        shutil.rmtree(folder_path)
        sys.exit(1)
    
    # Create Dockerfile if requested
    if dockerfile:
        create_dockerfile(folder_path)
        click.echo(click.style("✓ Created Dockerfile", fg="green"))
    
    # Summary
    click.echo("\n" + "="*50)
    click.echo(click.style("Flask app created successfully!", fg="green", bold=True))
    click.echo(f"Project location: {folder_path}")
    click.echo("\nTo run the app:")
    click.echo(f"  cd {folder_name}")
    click.echo("  pip install -r requirements.txt")
    click.echo("  python app.py")
    
    if dockerfile:
        click.echo("\nTo build and run with Docker:")
        click.echo("  docker build -t flask-clone .")
        click.echo("  docker run -p 5000:5000 flask-clone")
    
    click.echo("\nAccess the app at: http://localhost:5000")


@cli.command()
@click.argument("folder_name")
def run(folder_name):
    """Run an existing Flask clone app."""
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    if not os.path.exists(folder_path):
        click.echo(click.style(f"Error: Folder '{folder_name}' not found.", fg="red"))
        sys.exit(1)
    
    app_path = os.path.join(folder_path, "app.py")
    if not os.path.exists(app_path):
        click.echo(click.style(f"Error: app.py not found in '{folder_name}'.", fg="red"))
        sys.exit(1)
    
    click.echo(click.style(f"Starting Flask app from: {folder_path}", fg="cyan"))
    
    try:
        os.chdir(folder_path)
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        click.echo(click.style("\nApp stopped.", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"Error running app: {e}", fg="red"))




if __name__ == "__main__":create_flask_app_structure
    cli()