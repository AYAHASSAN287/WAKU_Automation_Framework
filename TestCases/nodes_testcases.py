import time
from unittest import TestCase
from Interfaces.waku_handler import WAKU_handler
import json
import logging
from logging_Custom.log_class import CustomFormatter

class TestCases_all():
    __test__ = False
    def __init__(self):
        urlstring="enrUri"
        self.waku=WAKU_handler()
        self.test=TestCase()
        with open('node1_config.json') as f:
            self.node1_config = json.load(f)
        with open('node2_config.json') as y:
            self.node2_config = json.load(y)
        with open('nodes_data.json') as m:
            self.nodes_data = json.load(m)
        self.node1_ports = [21161,21162,21163,21164]
        self.node2_ports=  [60000,9000,8646,8545]
        self.node1_rest_port=self.node1_config['listen-address']+":"+self.node1_config['rest-port']
        self.node2_rest_port=self.node2_config['listen-address']+":"+self.node2_config['rest-port']
        self.node1_ext_ip=self.node1_config['nat'].replace('extip:','')
        self.node2_ext_ip=self.node2_config['nat'].replace('extip:','')
        self.logger = logging.getLogger("My_app")
        self.logger.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(CustomFormatter())
        self.logger.addHandler(self.ch)
        self.logger.info(f"node1 & node2 configurations loaded from node1_config.json &node2_config.json")

    def test_default_precondition(self):
        self.logger.debug(f"precondition test case is empty")

    def test_default_postcondition(self,node_id):
        self.waku.waku_node_stop(node_id)
        self.logger.debug(f"container with id {node_id} stopped \n")

    def test_custom_postcondition(self,node_id,network):
        self.waku.waku_node_stop(node_id)
        self.waku.waku_network_stop(network)
        self.logger.debug(f"container with id {node_id} stopped \n network {network} stopped")

    def test_node_creation(self,image,node_name,node_options,ports):
        container=self.waku.waku_create_node(node_name,image,node_options,ports)
        self.logger.debug(f"node {node_name} created with options {node_options} \n image {image} is up ")
        return container

    def test_node_up(self,msg):
        self.logger.debug("node health check")

    def test_basic_node_operation(self):
        payload="UmVsYXkgd29ya3MhIQ"
        self.logger.debug(f"calling precondition test case")
        self.test_default_precondition()
        self.logger.debug(f"test precondition finished" )
        self.logger.debug(f"creating node {self.nodes_data['image']} from image {self.nodes_data['image']}")
        self.logger.debug(f"wait for timeout")
        container=self.test_node_creation(self.nodes_data['image'],"Node1",
                                    self.node1_config,self.node1_ports)
        time.sleep(5)
        self.logger.info(f"node 1 created successfully")
        result=self.waku.waku_get_node_debug_info(self.node1_rest_port)
        time.sleep(2)
        self.test.assertIn(self.node1_ext_ip,result,msg=f"error can't get debug info for"
                                            f" ip {self.node1_ext_ip}")
        self.logger.info(f"debug info fetched successfully")
        self.logger.debug(f"subscribing node of ip {self.node1_ext_ip} to topic {self.nodes_data['topic']}")
        result=self.waku.waku_node_subscrib(self.node1_rest_port,self.nodes_data['topic'])
        time.sleep(2)
        self.test.assertIn('OK',result,f"error in subscription please check if node up and rest "
                        f"port{self.node1_rest_port} is correct")
        self.logger.info(f"node with ip {self.node1_rest_port} subscribed successfully to topic "
                         f"{self.nodes_data['topic']}")
        self.logger.debug(f"sending msg {payload} for node1")
        self.logger.debug(f"waiting for timeout")
        result=self.waku.waku_send_msg(self.node1_rest_port,payload,self.nodes_data['topic'])
        time.sleep(2)
        self.test.assertIn('OK',result,f"error in sending message please check if node up and rest "
                                       f"port{self.node1_rest_port} is correct")
        self.logger.info(f"node with ip {self.node1_rest_port} successfully send message {payload}")
        self.logger.debug(f"check if message can be retrieved ")
        result=self.waku.waku_get_msg(self.node1_rest_port,self.nodes_data['topic'])
        self.test.assertIn(payload,result,msg=f"error message isn't fond")
        self.logger.info(f"message {payload} is sent and retrieved successfully")
        self.logger.debug(f"stop the container {container.short_id}of node1 ")
        self.logger.info("Test case Passed")
        self.test_default_postcondition(container.short_id)

    def test_Inter_Node_Communication(self):
        payload="UmVsYXkgd29ya3MhIQ"
        self.logger.debug(f"calling precondition test case")
        self.test_default_precondition()
        self.logger.debug(f"test precondition finished" )
        self.logger.debug(f"creating node {self.nodes_data['image']} from image {self.nodes_data['image']}")
        self.logger.debug(f"wait for timeout")
        container_node1=self.test_node_creation(self.nodes_data['image'],"Node1",
                                          self.node1_config,self.node1_ports)
        time.sleep(5)
        self.logger.info(f"node 1 created successfully")
        result=self.waku.waku_get_node_debug_info(self.node1_rest_port)
        time.sleep(2)
        self.test.assertIn(self.node1_ext_ip,result,msg=f"error can't get debug info for"
                                                        f" ip {self.node1_ext_ip}")

        self.logger.debug(f"subscribing node of ip {self.node1_ext_ip} to topic {self.nodes_data['topic']}")
        result=self.waku.waku_node_subscrib(self.node1_rest_port,self.nodes_data['topic'])
        time.sleep(2)
        self.test.assertIn('OK',result,f"error in subscription please check if node up and rest "
                                f"port{self.node1_rest_port} is correct")

        self.logger.info(f"node with ip {self.node1_rest_port} subscribed successfully to topic "
                    f"{self.nodes_data['topic']}")

        self.logger.debug(f"add node to network {self.nodes_data['network-name']} with subnet "
                    f"{self.nodes_data['network-subnet']} and gateway {self.nodes_data['network-gateway']}")

        self.waku.waku_create_network(self.nodes_data['network-subnet'],self.nodes_data['network-gateway'],
                                    self.nodes_data['network-name'])
        time.sleep(3)
        self.logger.info(f"network created successfully")
        self.logger.debug(f"adding node1 to the network {self.nodes_data['network-name']}")
        self.waku.waku_add_node_tonetwork(self.node1_ext_ip,self.nodes_data['network-name'],
                                        container_node1.short_id)
        time.sleep(4)
        result=self.waku.waku_network_inspect(self.nodes_data['network-name'])
        time.sleep(3)
        self.test.assertIn(self.node1_ext_ip,result,msg=f"error ! node isn't connected to the network")
        self.logger.info(f"node added successfully")
        #node2
        self.logger.debug(f"configuring node2")
        self.node2_config['discv5-bootstrap-node']=self.waku.waku_get_node_enrUri(self.node1_rest_port)

        result=self.waku.waku_get_node_enrUri(self.node1_rest_port)
        time.sleep(3)
        self.logger.debug(f"creating node {self.nodes_data['image']} from image {self.nodes_data['image']}")
        self.logger.debug(f"wait for timeout")

        container_node2=self.test_node_creation(self.nodes_data['image'],"Node2",
                                        self.node2_config,self.node2_ports)

        time.sleep(3)
        self.logger.info(f"node 2 created successfully")
        result=self.waku.waku_get_node_debug_info(self.node2_rest_port)
        time.sleep(2)
        self.test.assertIn(self.node2_ext_ip,result,msg=f"error can't get debug info for"
                                 f" ip {self.node2_ext_ip}")

        self.logger.info(f"debug info fetched successfully")
        self.waku.waku_add_node_tonetwork(self.node2_ext_ip,self.nodes_data['network-name'],
                                     container_node2.short_id)
        time.sleep(10)
        result=self.waku.waku_network_inspect(self.nodes_data['network-name'])
        time.sleep(3)
        self.test.assertIn(self.node2_ext_ip,result,msg=f"error ! node isn't connected to the network")
        self.logger.info(f"node added successfully")

        self.logger.debug(f"Test if node2 added as peer for node1")
        node_peers=self.waku.waku_get_node_peers(self.node1_rest_port)
        time.sleep(2)
        self.test.assertIn(self.node2_ext_ip,node_peers)
        self.logger.info(f"node2 addedd successfully as peer to node1")
        self.logger.debug(f"subcribe node2 to topic {self.nodes_data['topic']}")
        time.sleep(3)
        result=self.waku.waku_node_subscrib(self.node2_rest_port,self.nodes_data['topic'])
        self.test.assertIn('OK',result,f"error in subscription please check if node up and rest "
                                       f"port{self.node2_rest_port} is correct")

        self.logger.debug(f"sending msg {payload} for node1")
        self.logger.debug(f"waiting for timeout")
        result=self.waku.waku_send_msg(self.node1_rest_port,payload,
                                       self.nodes_data['topic'])
        time.sleep(6)
        self.test.assertIn('OK',result,f"error in sending message please check if node up and rest "
                                       f"port{self.node1_rest_port} is correct")
        self.logger.info(f"node with ip {self.node1_rest_port} successfully send message {payload}")
        self.logger.debug(f"check if message received by node2 ")
        result=self.waku.waku_get_msg(self.node2_rest_port,self.nodes_data['topic'])
        self.test.assertIn(payload,result,msg=f"error message isn't fond")
        self.logger.info(f"message {payload} is received  successfully by node2")
        self.logger.debug(f"stop the container {container_node1.short_id}of node1\n"
                          f" stop the container {container_node2.short_id}of node2")
        self.test_default_postcondition(container_node1.short_id)
        self.logger.info("Test case Passed")
        self.test_custom_postcondition(container_node2.short_id,self.nodes_data['network-name'])















