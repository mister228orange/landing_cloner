import docker


def url2singlefile(url:str) -> str:
    client = docker.from_env()  # Create a client instance from environment variables
    
    try:
        image = client.images.pull("capsulecode/singlefile")  # Pull the required Docker image
        
        container = client.containers.run(image, url)  # Run the image in a new container
        
        html_content = container.decode() # Get HTML content from the running container
    except docker.errors.APIError as e:
        print(f"Docker error: {e}")
        raise "Downloading error"
    
    return html_content


file = url2singlefile("https://oneman4rmy.carrd.co")
print(file)
