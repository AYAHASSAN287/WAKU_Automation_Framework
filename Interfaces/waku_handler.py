import time
from dataclasses import dataclass
import logging
import sys
from Interfaces.rest_handler import RestInterface
from Interfaces.docker_handler import DockerHandler
import subprocess
class WAKU_handler:

    def __init__(self):
        self.node_containers={}
        self.dock=DockerHandler()
        self.rest=RestInterface()

    def waku_create_node(self,node_name,image,command,ports):
        command_config=list()
        port_format= list()
        self.node_containers={}
        for i, j in command.items():

            command_config.append(f"--{i}={j}")       # The port number, as an integer. For example, {'2222/tcp': 3333} will expose port 2222 inside the container as port 3333 on the host. from docker python sdk
        port_format={f"{port}/tcp": ("", port) for port in ports}
        try:
            container=self.dock.docker_create_start_container(image,command_config,port_format)
            self.node_containers[node_name]=container.short_id
            return container
        except:
            raise Exception("error container isn't created")

    def waku_get_node_debug_info(self,node_address):

        return self.rest.rest_get_debug_info(node_address)

    def waku_node_subscrib(self,node_address,topic):
        try:
            return self.rest.rest_post_subscrib(node_address,topic)
        except:
            raise Exception("error node %s can't subscrib to topic %s",node_address
                            ,topic)

    def waku_send_msg(self,node_address,payload,topic):
        try:
            return self.rest.rest_send_message(node_address,payload,topic)
        except:
            raise Exception("error node %s can't send msg %s",node_address
                            ,payload)

    def waku_get_msg(self,node_address,topic):
        try:
            return self.rest.rest_get_msg_response(node_address,topic)
        except:
            raise Exception("error node %s can't get msg from topic %s",node_address
                            ,topic)

    def waku_create_network(self,network_subnet,gateway,network_name):
        try:
            self.dock.docker_create_network(network_subnet,gateway,network_name)
        except:
            raise Exception(" failed to create network  %s",network_name)

    def waku_add_node_tonetwork(self,container_ip,network_name,container_id):
        try:
            self.dock.docker_add_container_network(container_ip,network_name,container_id)
        except:
            raise Exception(" failed to add node of ip %s to network %s",container_ip
                            ,network_name)

    def waku_get_node_enrUri(self,node_ip):
        return self.rest.rest_get_enrUri_info(node_ip)

    def waku_get_node_peers(self,node_ip):
        return self.rest.rest_get_peers(node_ip)

    def waku_node_stop(self,node_id):
        return self.rest.rest_stop_node(node_id)

    def waku_network_stop(self,network):
        return self.rest.rest_stop_network(network)

    def waku_network_inspect(self,network_name):
        return self.rest.rest_network_inspect(network_name)