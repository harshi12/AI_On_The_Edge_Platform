from queue_req_resp import RabbitMQ
import time
from threading import Thread
from Registry_API import Registry_API
import json
# load_at_hosts = {"service1":[["ip1",44,"yes"],["ip2",22,"no"]],"service2":[["ip1",12,"yes"]]}
load_at_hosts = {}
host_credentials = {}
new_load_at_hosts = {}
new_load_at_hosts2 = {}
perm_list_of_ips = []
pool_list = {}
pool_list2 = {}
pool={}
upper_threshold = 60
msg_obj = RabbitMQ("192.168.31.244", "harshita", "123", 5672)
reg_obj = Registry_API("192.168.31.244",5672,"harshita", "123")

def getting_host_credentials():
    reg_obj.Read_Host_Creds("","LBHC_RG","RG_LBHC")

def reload_interval():
    value = "no"
    load = 0
    pool_list = {k:load for k in perm_list_of_ips}
    pool_list2 = {k:value for k in perm_list_of_ips}

def get_current_status_from_registry():
    reg_obj.Read_Service_Inst_Info("","LBSI_RG","RG_LBSI")

# should be running on seperate thread to continuously update data structure
def read_current_status_from_registry(load_at_hosts):
    list_of_services = list(load_at_hosts)
    for i in list_of_services:
        list_of_ips = load_at_hosts[i]
        y = len(list_of_ips)
        for j in range(y):
            ip_check = list_of_ips[j][0]
            where_to_check = new_load_at_hosts[i]
            if ip_check in where_to_check:
                continue
            else:
                new_load_at_hosts[i][list_of_ips[j][0]]=0
            if list_of_ips[j][0] not in perm_list_of_ips:
                perm_list_of_ips.append(list_of_ips[j][0])
                new_load_at_hosts2[list_of_ips[j][0]]={}
            if i not in new_load_at_hosts2[list_of_ips[j][0]]:
                new_load_at_hosts2[list_of_ips[j][0]][i] = list_of_ips[j][3]
    reload_interval()

def load_calculation():
    list_of_services = list(new_load_at_hosts)
    for i in list_of_services:
        list_of_ips = new_load_at_hosts[i]
        y = len(list_of_ips)
        for j in list_of_ips:
            if pool_list2[j] == "no":
                ip = j
                username = host_credentials[ip]["Username"]
                password = host_credentials[ip]["Password"]
                query = "sshpass -p '"+password+"' ssh "+username+"@"+ip+" grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' "
                x = subprocess.check_output(query,shell=True)
                x = x.decode("utf-8")
                x = float(x)
                new_load_at_hosts[i][j] = x
                pool_list[j] = x
                pool_list2[j] = "yes"
            else:
                new_load_at_hosts[i][j] = pool_list[j]
    # sort the list based on load for each service TO DO
        xx = new_load_at_hosts[i]
        xx = sorted(xx.items(), key=lambda item: item[1])
        xx = dict(xx)
        new_load_at_hosts[i] = xx
        pool_list = sorted(pool_list.items(), key=lambda item: item[1])
        pool_list = dict(pool_list)
        print("new_load_at_hosts")
        print(new_load_at_hosts)
        print("pool_list")
        print(pool_list)

def handle_deployment_manager_request(number_of_instances):
    response = []
    n = len(pool_list)
    i = 0
    l = list(pool_list)
    while i<n and number_of_instances>0:
        if pool_list[l[i]]<upper_threshold:
            response.append(l[i])
            number_of_instances -= 1
            i += 1
        else:
            break
    k = 0
    itr = 0
    while k<number_of_instances:
        if pool[list(pool)[itr]] == 'available':
            response.append(list(pool)[itr])
            pool[list(pool)[itr]] = 'allotted'
            itr += 1
            k += 1
        else:
            itr += 1
    return response


def handle_service_manager_request():
    list_of_services = list(new_load_at_hosts)
    response = {}
    for i in list_of_services:
        response[i]=new_load_at_hosts[i].keys()[0]
    return response


def thread_func():
    while True:
        get_current_status_from_registry()
        time.sleep(10)

def hm_callback(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')

    #Receiving_Message = json.loads(body).replace('\'','\"')
    Receiving_Message = json.loads(body)
    print("\nReceiving_Message: ", Receiving_Message)

    No_Instances = Receiving_Message["No_Instances"]
    response = handle_deployment_manager_request(No_Instances)

    json_response = json.dumps(response)
    msg_obj.send("", "LB_HM", json_response)

def Recieve_from_HM():
    msg_obj.receive(hm_callback, "", "HM_LB")

def rg_hc_callback(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    host_credentials = json.loads(body)
    print("\nReceiving_Message from registry: ", host_credentials)

    print(host_credentials)
    l1 = list(host_credentials)
    pool = {k:"available" for k in l1}

def Recieve_from_RG_HC():
    msg_obj.receive(rg_hc_callback, "", "RG_LBHC")


def rg_si_callback(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    # host_credentials = json.loads(body)
    # print("\nReceiving_Message from registry: ", host_credentials)
    #
    # print(host_credentials)
    # l1 = list(host_credentials)
    # pool = {k:"available" for k in l1}
    service_info = json.loads(body)
    print("\nReceiving_Message from registry: ",service_info )
    print(service_info)
    read_current_status_from_registry(service_info)
    load_calculation()

def Recieve_from_RG_SI():
    msg_obj.receive(rg_si_callback, "", "RG_LBSI")


def sm_send(ch, method, properties, body):
    while True:
        response = handle_service_manager_request()
        json_response = json.dumps(response)
        msg_obj.send("", "LB_SM", json_response)
        time.sleep(10)


def load_balance():
    # check for upsacling
    rev_pool_list = sorted(pool_list.items(), key=lambda item: item[1], reverse = True)
    rev_pool_list = dict(rev_pool_list)
    for i in rev_pool_list:
        if rev_pool_list[i]>=upper_threshold:
            list_of_services_pids = new_load_at_hosts2[i]
            pid_loads = {}
            for j in list_of_services_pids:
                pid = list_of_services_pids[j]
                ip = i
                username = host_credentials[ip]["Username"]
                password = host_credentials[ip]["Password"]
                query = "sshpass -p '"+password+"' ssh "+username+"@"+ip+" ps -p "+pid+" -o %cpu"
                x = subprocess.check_output(query,shell=True)
                x = x.decode("utf-8")
                x = x.split("\n")
                x = float(x[1])
                pid_loads[pid] = x
            pid_loads = sorted(pid_loads.items(), key=lambda item: item[1],reverse = True)
            pid_loads = dict(pid_loads)
            first_pid = next(iter(pid_loads))
            service_id_to_be_migrated = dict((v,k) for k, v in list_of_services_pids.items())[first_pid]
            # send request to service manager to down the service
            # send request to host manager to up the service on a new host
    # check for downscaling


if __name__ == '__main__':

    getting_host_credentials()
    # reload_interval()
    t_lb = Thread(target=thread_func)
    t_lb.start()

    # msg_obj.create_ServiceQueues("LB", "HM")
    msg_obj.create_queue('',"LBHC_RG")
    msg_obj.create_queue('',"RG_LBHC")
    msg_obj.create_queue('',"LBSI_RG")
    msg_obj.create_queue('',"RG_LBSI")
    msg_obj.create_queue('',"LB_SM")

    t_hm = Thread(target=Recieve_from_HM)
    t_hm.start()

    t_sm = Thread(target=sm_send)
    t_sm.start()

    t_rg_hc = Thread(target=Recieve_from_RG_HC)
    t_rg_hc.start()

    t_rg_si = Thread(target=Recieve_from_RG_SI)
    t_rg_si.start()

# this portion is for upsacling and downscaling. To be done later.
# for i in perm_list_of_ips:
#     load = pool_list[i]
#     if load >= upper_threshold:
#         ip = i
#         list_of_services = list(new_load_at_hosts)
#         for i in range(len(list_of_services)):
#             list_of_ips = new_load_at_hosts[list_of_services[i]]
#             for j in range(len(list_of_ips)):
#                 if ip == list_of_ips[j][0]:
#                     # move service to another
#     else:
#
#             change status to available
#         else
#             nothing
