import sys
import os
import docker
import subprocess


class DockerHandler:

    def __init__(self):
        #self.image_name=image_name
        self.dock=docker.from_env()
        ipam_pool = docker. types. IPAMPool( subnet='192.168.52.0/ 24', gateway='192.168.52.254' )


    def docker_create_start_container(self,image_name, command, ports):

        container=self.dock.containers.run(image_name,command=command,ports=ports,detach=True)
        return container


    def docker_create_network(self,network_subnet,network_gateway,network_name):

        ipam_pool = docker.types.IPAMPool( subnet=network_subnet, gateway=network_gateway )
        ipam_config = docker.types.IPAMConfig( pool_configs=[ipam_pool])
        try:
            network_config=self.dock.networks.create(network_name,driver="bridge", ipam=ipam_config)
            return network_config
        except:
            raise Exception("error creating image %s ",sys.stderr)






    def docker_add_container_network(self,container_ip,network,container_id):
        command = "docker network connect --ip "
        result=subprocess.run(f"docker network connect --ip  { container_ip} {network} {container_id}",shell=True)
        #print(result.stdout)





