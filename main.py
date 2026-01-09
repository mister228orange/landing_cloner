import os
import click
import subprocess
import sys
from utils import create_dockerfile, create_server, get_folder_name
from server_builder import build_server


@click.group(invoke_without_command=True)
@click.option("-p", "--path", help="URL of the web page to clone.")
@click.option("--name", "-n", help="Custom name for the project folder.")
@click.option("--dockerfile", "-d", is_flag=True, help="Generate a Dockerfile.", default=False)
@click.pass_context
def cli(ctx, path, file, name, dockerfile, force):
    """Flask Clone CLI - Create Flask apps from web pages or local HTML files.
    
    Examples:
    
      landing_cloner clone https://example.com
      landing_cloner up_file ./page.html -n myapp
      landing_cloner clone https://example.com -p ../path/to/project -d

    """
    # If no subcommand is invoked and we have path or file, run main functionality
    if ctx.invoked_subcommand is None:
        if path or file:
            ctx.invoke(main_func, path=path, file=file, name=name, 
                       dockerfile=dockerfile, force=force)
        else:
            click.echo(ctx.get_help())



@cli.command("clone")
@click.argument("url")
@click.option("-p", "--path", help="URL of the web page to clone.")
@click.option("--name", "-n", help="Custom name for the project folder.")
@click.option("--dockerfile", "-d", is_flag=True, help="Generate a Dockerfile.", default=False)
def clone(url, name=None, dockerfile=False):
    """Create a Flask app from a cloned web page."""
    html_content = url2file(url)


    # Determine folder name
    folder_name = name if name else get_folder_name(url)
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Check if folder exists
    if os.path.exists(folder_path):
        click.echo(click.style(f"Error: Folder '{folder_name}' already exists.", fg="red"))
        sys.exit(1)
    
    click.echo(click.style(f"Creating Flask app from: {url}", fg="cyan"))
    click.echo(click.style(f"Project folder: {folder_path}", fg="cyan"))
    
    build_server(folder_path, html_content)

    

@cli.command("up_file")
@click.argument("folder_name")
@click.option("-p", "--path", help="URL of the web page to clone.")
@click.option("--name", "-n", help="Custom name for the project folder.")
@click.option("--dockerfile", "-d", is_flag=True, help="Generate a Dockerfile.", default=False)
def run(folder_name):
    """Serve an existing HTML File."""
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    if not os.path.exists(folder_path):
        click.echo(click.style(f"Error: Folder '{folder_name}' not found.", fg="red"))
        sys.exit(1)
    
    html_page = open(folder_path, 'r').read()
    
    click.echo(click.style(f"Starting Flask app from: {folder_path}", fg="cyan"))
    try:
        os.chdir(folder_path)
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        click.echo(click.style("\nApp stopped.", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"Error running app: {e}", fg="red"))




if __name__ == "__main__":
    create_flask_app_structure()
    cli()