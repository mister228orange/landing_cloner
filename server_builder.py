import os
import click
import sys
from utils import create_dockerfile

def build_server(folder_path, html_content, dockerfile=False):
    # Create folder
    try:
        os.makedirs(folder_path)
        click.echo(click.style("✓ Created project folder", fg="green"))
    except OSError as e:
        click.echo(click.style(f"Error creating folder: {e}", fg="red"))
        sys.exit(1)
    
    
    # Create Flask app structure
    try:
        create_server(folder_path, html_content)
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
