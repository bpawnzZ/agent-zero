import time
import docker
import atexit
from typing import Optional
from python.helpers.files import get_abs_path
from python.helpers.errors import format_error
from python.helpers.print_style import PrintStyle
from python.helpers.log import Log

class DockerContainerManager:
    def __init__(self, logger: Log, name: str, image: str, ports: dict, volumes: dict):
        self.logger = logger
        self.name = name
        self.image = image
        self.ports = ports
        self.volumes = volumes
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.container = None
        self.init_docker()
                
    def init_docker(self):
        self.client = None
        while not self.client:
            try:
                self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
                self.container = None
            except Exception as e:
                err = format_error(e)
                if ("ConnectionRefusedError(61," in err or "Error while fetching server API version" in err):
                    PrintStyle.hint("Connection to Docker failed. Is docker or Docker Desktop running?") # hint for user
                    if self.logger:self.logger.log(type="hint", content="Connection to Docker failed. Is docker or Docker Desktop running?")
                    PrintStyle.error(err)
                    if self.logger:self.logger.log(type="error", content=err)
                    time.sleep(5) # try again in 5 seconds
                else: raise
        return self.client
                            
    def cleanup_container(self) -> None:
        if self.container:
            try:
                self.container.stop()
                self.container.remove()
                PrintStyle.standard(f"Stopped and removed the container: {self.container.id}")
                if self.logger: self.logger.log(type="info", content=f"Stopped and removed the container: {self.container.id}")
            except Exception as e:
                PrintStyle.error(f"Failed to stop and remove the container: {e}")
                if self.logger: self.logger.log(type="error", content=f"Failed to stop and remove the container: {e}")

    def get_image_containers(self):
        if not self.client: self.client = self.init_docker()
        containers = self.client.containers.list(all=True, filters={"ancestor": self.image})
        infos = []
        for container in containers:
            infos.append({                
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image,
                "ports": container.ports,
                "web_port": (container.ports.get("80/tcp") or [{}])[0].get("HostPort"),
                "ssh_port": (container.ports.get("22/tcp") or [{}])[0].get("HostPort"),
                # "volumes": container.volumes,
                # "data_folder": container.volumes["/a0"],
            })
        return infos

    def start_container(self):
        try:
            self.container = self.client.containers.get(self.name)
        except docker.errors.NotFound:
            self.container = self.client.containers.run(
                self.image,
                name=self.name,
                ports=self.ports,
                volumes=self.volumes,
                detach=True
            )

    async def exec_command(self, command: str) -> str:
        if not self.container:
            raise Exception("Container not started")
            
        result = self.container.exec_run(
            command,
            workdir="/a0",
            demux=True
        )
        
        output = ""
        if result.output[0]:  # stdout
            output += result.output[0].decode('utf-8')
        if result.output[1]:  # stderr
            output += result.output[1].decode('utf-8')
            
        return output

    def stop_container(self):
        if self.container:
            self.container.stop()
            self.container = None
