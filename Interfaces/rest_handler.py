import subprocess

class RestInterface:

    def __init__(self):

        print("rest class is up")

    def rest_get_debug_info(self, ip_address):
        result = subprocess.check_output(f"curl -X GET http://{ip_address}/debug/v1/info",shell=True)

        return result.decode("utf-8")

    def rest_get_enrUri_info(self, ip_address):
        enrurl: str = ""
        result = subprocess.check_output(f"curl -X GET {ip_address}/debug/v1/info",shell=True)
        res=result.partition(b'enrUri":"')
        enrurl=res[2].decode("utf-8")
        enrurl=enrurl[:-2]
        return enrurl


    def rest_check_node_health(self, ip_address):
        print("health")

    def rest_post_subscrib(self, ip_address,topic):
        result = subprocess.check_output(f"curl -X POST http://{ip_address}/relay/v1/auto/subscriptions\
         -H \"accept: text/plain\" -H \"content-type: application/json\" -d '[\"{topic}\"]'",shell=True)
        return result.decode("utf-8")

    def rest_send_message(self, ip_address, payload,topic):
        command: str = ("curl -X POST \"http://"+str(ip_address)+"/relay/v1/auto/messages\""
                        " -H \"content-type: application/json\" -d '{\"payload\":\""+str(payload)+
                        "==\",\"contentTopic\":\""
                        +str(topic)+"\",\"timestamp\":0}'"
                        )
        result = subprocess.check_output(command,shell=True)
        return result.decode("utf-8")



    def rest_get_msg_response(self, ip_address,topic):
        str_topic :str=topic
        topic_format=str_topic.replace("/","%2f")
        result = subprocess.check_output(f"curl -X GET {ip_address}/relay/v1/auto/messages/{topic_format}",shell=True)

        return result.decode("utf-8")

    def rest_get_peers(self, ip_address):
        result = subprocess.check_output(f"curl -X GET http://{ip_address}/admin/v1/peers",shell=True)
        return result.decode("utf-8")

    def rest_stop_node(self,node_id):
        return subprocess.check_output(f"docker stop {node_id}",shell=True)

    def rest_stop_network(self,network_name):
        result= subprocess.check_output(f"docker network remove {network_name}",shell=True)
        return result.decode("utf-8")

    def rest_network_inspect(self,network_name):
        result = subprocess.check_output(f"docker network inspect {network_name}",shell=True)
        return result.decode("utf-8")






