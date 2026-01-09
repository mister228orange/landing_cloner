import docker


def url2singlefile(url:str) -> str:
    image = docker.APIClient.pull("capsulecode", "singlefile")
    container = docker.api.APIClient.build(image)
    html = docker.APIClient.start(container=container)
    return html

url2singlefile("vk.com")
