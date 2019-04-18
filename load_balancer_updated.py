from queue_req_resp import RabbitMQ
import time
from threading import Thread
from Registry_API import Registry_API
import json
import subprocess
# load_at_hosts = {"service1":[["ip1",44,"yes"],["ip2",22,"no"]],"service2":[["ip1",12,"yes"]]}
load_at_hosts = {}
host_credentials = {}
new_load_at_hosts = {}
new_load_at_hosts2 = {}
perm_list_of_ips = []
pool_list = {}
pool_list2 = {}
pool={}
service_ids = []
upper_threshold = 60
lower_threshold = 2
upper_queue_threshold = 10
lower_queue_threshold = -1
msg_obj = RabbitMQ("10.2.135.82", "harshita", "123", 5672)
reg_obj = Registry_API("10.2.135.82",5672,"harshita", "123")

def getting_host_credentials():
    reg_obj.Read_Host_Creds("","LBHC_RG","RG_LBHC")

# def reload_interval():
#     value = "no"
#     load = 0
#     pool_list = {k:load for k in perm_list_of_ips}
#     pool_list2 = {k:value for k in perm_list_of_ips}

def get_current_status_from_registry():
    reg_obj.Read_Service_Inst_Info("","LBSI_RG","RG_LBSI")

# should be running on seperate thread to continuously update data structure
def read_current_status_from_registry(load_at_hosts):
    global new_load_at_hosts
    global new_load_at_hosts2
    global perm_list_of_ips
    list_of_services = list(load_at_hosts)
    for i in list_of_services:
        if i not in service_ids:
            service_ids.append(i)
        list_of_ips = load_at_hosts[i]
        y = len(list_of_ips)
        if i not in new_load_at_hosts:
            new_load_at_hosts[i]={}
        for j in range(y):
            ip_check = list_of_ips[j][0]
            ip_status = list_of_ips[j][2]
            where_to_check = new_load_at_hosts[i]
            if ip_status == "Up":
                if ip_check not in new_load_at_hosts2:
                    new_load_at_hosts2[list_of_ips[j][0]] = {}
            if ip_check in where_to_check:
                if ip_status == "Down":
                    if (list_of_ips[j][3],list_of_ips[j][5]) in new_load_at_hosts[i][ip_check]:
                        new_load_at_hosts[i][ip_check].remove((list_of_ips[j][3],list_of_ips[j][5]))
                    if i in new_load_at_hosts2[list_of_ips[j][0]]:
                        if (list_of_ips[j][3],list_of_ips[j][5]) in new_load_at_hosts2[list_of_ips[j][0]][i]:
                            new_load_at_hosts2[list_of_ips[j][0]][i].remove((list_of_ips[j][3],list_of_ips[j][5]))
                else:
                    if (list_of_ips[j][3],list_of_ips[j][5]) not in new_load_at_hosts[i][ip_check]:
                        new_load_at_hosts[i][ip_check].append((list_of_ips[j][3],list_of_ips[j][5]))
                    if i in new_load_at_hosts2[list_of_ips[j][0]]:
                        if (list_of_ips[j][3],list_of_ips[j][5]) not in new_load_at_hosts2[list_of_ips[j][0]][i]:
                            new_load_at_hosts2[list_of_ips[j][0]][i].append((list_of_ips[j][3],list_of_ips[j][5]))
                    else:
                        new_load_at_hosts2[list_of_ips[j][0]][i] = []
                        if (list_of_ips[j][3],list_of_ips[j][5]) not in new_load_at_hosts2[list_of_ips[j][0]][i]:
                            new_load_at_hosts2[list_of_ips[j][0]][i].append((list_of_ips[j][3],list_of_ips[j][5]))
            else:
                if ip_status == "Up":
                    new_load_at_hosts[i][list_of_ips[j][0]]=[]
                    if (list_of_ips[j][3],list_of_ips[j][5]) not in new_load_at_hosts[i][ip_check]:
                        new_load_at_hosts[i][ip_check].append((list_of_ips[j][3],list_of_ips[j][5]))
                    if i in new_load_at_hosts2[list_of_ips[j][0]]:
                        if (list_of_ips[j][3],list_of_ips[j][5]) not in new_load_at_hosts2[list_of_ips[j][0]][i]:
                            new_load_at_hosts2[list_of_ips[j][0]][i].append((list_of_ips[j][3],list_of_ips[j][5]))
                    else:
                        new_load_at_hosts2[list_of_ips[j][0]][i] = []
                        new_load_at_hosts2[list_of_ips[j][0]][i].append((list_of_ips[j][3],list_of_ips[j][5]))

                if list_of_ips[j][0] not in perm_list_of_ips:
                    perm_list_of_ips.append(list_of_ips[j][0])

    print("new_load_at_hosts")
    print(new_load_at_hosts)
    print("new_load_at_hosts2")
    print(new_load_at_hosts2)
    print("perm_list_of_ips")
    print(perm_list_of_ips)


    # reload_interval()

def load_calculation():
    global pool_list
    global perm_list_of_ips
    memory_consumption = {}
    for ip in perm_list_of_ips:
        username = host_credentials[ip]["Username"]
        password = host_credentials[ip]["Password"]
        query = "sshpass -p '"+password+"' ssh -o \"StrictHostKeyChecking no\" "+username+"@"+ip+" grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' "
        x = subprocess.check_output(query,shell=True)
        x = x.decode("utf-8")
        x = float(x)
        pool_list[ip] = x
    pool_list = sorted(pool_list.items(), key=lambda item: item[1])
    pool_list = dict(pool_list)
    # for ip in perm_list_of_ips:
    #     memory_consumption[ip] = 0
    #     for service in new_load_at_hosts2[ip]:
    #         entries = new_load_at_hosts2[ip][service]
    #         pids = [x[0] for x in entries]
    #         for pid in pids:
    #             query = "sshpass -p '"+password+"' ssh -o \"StrictHostKeyChecking no\" "+username+"@"+ip+" ps -p "+pid+" -o %mem"
    #             y = subprocess.check_output(query,shell=True)
    #             y = y.decode("utf-8")
    #             y = float(y)
    #             memory_consumption[ip] = memory_consumption[ip] + y
    print("cpu utilization")
    print(pool_list)
    # print("memory consumption")
    # print(memory_consumption)

def handle_host_manager_request(number_of_instances):
    global host_credentials
    number_of_instances = int(number_of_instances)
    response = {}
    n = len(pool_list)
    i = 0
    l = list(pool_list)
    while i < n and number_of_instances > 0:
        if pool_list[l[i]]<=upper_threshold and pool_list[l[i]]>=lower_threshold:
            # response.append(l[i])
            response[l[i]]=[host_credentials[l[i]]["Username"],host_credentials[l[i]]["Password"]]
            number_of_instances -= 1
            i += 1
        else:
            break
    k = 0
    itr = 0
    while k<number_of_instances:
        if pool[list(pool)[itr]] == 'available':
            # response.append(list(pool)[itr])
            response[l[i]]=[host_credentials[list(pool)[itr]]["Username"],host_credentials[list(pool)[itr]]["Password"]]
            pool[list(pool)[itr]] = 'allotted'
            itr += 1
            k += 1
        else:
            itr += 1
    print("response to host manager")
    print(response)
    return response


def thread_func():
    get_current_status_from_registry()


def hm_callback(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')

    #Receiving_Message = json.loads(body).replace('\'','\"')
    Receiving_Message = json.loads(body)
    print("\nReceiving_Message: ", Receiving_Message)

    No_Instances = Receiving_Message["Number"]
    response = handle_host_manager_request(No_Instances)

    json_response = json.dumps(response)
    msg_obj.send("", "LB_HM", json_response)

# def hms_callback(ch, method, properties, body):
#     body = body.decode("utf-8").replace('\0', '')
#
#     #Receiving_Message = json.loads(body).replace('\'','\"')
#     Receiving_Message = json.loads(body)
#     print("\nReceiving_Message: ", Receiving_Message)
#
#     No_Instances = Receiving_Message["Number"]
#     response = handle_host_manager_request(No_Instances)
#
#     json_response = json.dumps(response)
#     msg_obj.send("", "LB_HMS", json_response)
#
# def hmm_callback(ch, method, properties, body):
#     body = body.decode("utf-8").replace('\0', '')
#
#     #Receiving_Message = json.loads(body).replace('\'','\"')
#     Receiving_Message = json.loads(body)
#     print("\nReceiving_Message: ", Receiving_Message)
#
#     No_Instances = Receiving_Message["Number"]
#     response = handle_host_manager_request(No_Instances)
#
#     json_response = json.dumps(response)
#     msg_obj.send("", "LB_HMM", json_response)

def Recieve_from_HM():
    msg_obj.receive(hm_callback, "", "HM_LB")

# def Recieve_from_HMS():
#     msg_obj.receive(hms_callback, "", "HM_LBS")
#
# def Recieve_from_HMM():
#     msg_obj.receive(hmm_callback, "", "HM_LBM")

def rg_hc_callback(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    global host_credentials
    global pool
    host_credentials = json.loads(body)
    print("\nReceiving_Message from registry: ", host_credentials)
    print("HOST CREDS")
    # print(host_credentials['192.168.31.34']["Username"])
    print(host_credentials)
    l1 = list(host_credentials)
    pool = {k:"available" for k in l1}

    t_lb1 = Thread(target=thread_func)
    t_lb1.start()

    t_lb2 = Thread(target=load_balance)
    t_lb2.start()


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

    time.sleep(30)
    thread_func()


def Recieve_from_RG_SI():
    msg_obj.receive(rg_si_callback, "", "RG_LBSI")


# def sm_send():
#     while True:
#         time.sleep(10)
#         response = handle_service_manager_request()
#         json_response = json.dumps(response)
#         msg_obj.send("", "LB_SM", json_response)


def load_balance():
    while 1:
        time.sleep(60)
        service_upscaling()
        host_upscaling()
        service_downscaling()
        host_downscaling()


def host_upscaling():
    global pool_list
    global pool
    global new_load_at_hosts
    global new_load_at_hosts2
    rev_pool_list = sorted(pool_list.items(), key=lambda item: item[1], reverse = True)
    rev_pool_list = dict(rev_pool_list)
    free_ip = None
    for i in rev_pool_list:
        if rev_pool_list[i]>=upper_threshold:
            itr = 0
            while itr < len(pool):
                if pool[list(pool)[itr]] == 'available':
                    free_ip = list(pool)[itr]
                    pool[list(pool)[itr]] = 'allotted'
                    break
                itr += 1
            # if free_ip = None:
            #     # do nothing
            # if we have a free host
            list_of_services_to_be_migrated = new_load_at_hosts2[i]
            for each_service in list_of_services_to_be_migrated:
                entries = new_load_at_hosts2[i][each_service]
                instance_ids = [x[1] for x in entries]
                no_of_instances = len(set(instance_ids))
                request_MT = {"Request_Type": "Gateway_Deploy","Service_ID" : each_service,"IPs":free_ip}
                msg_obj.send("","LBB_HM",request_MT)
                            # thread to listen to be written + ip to be sent

def service_upscaling():
    global service_ids
    for service_id in service_ids:
        queue_name = "PlatformInputStream_"+service_id
        length_of_queue = msg_obj.queue_length('',queue_name)
        if length_of_queue >= upper_queue_threshold:
            request_MT = {"Request_Type": "Service_Submit","Service_ID" : service_id,"Instances" : 1}
            msg_obj.send("","LBB_HM",request_MT)

def host_downscaling():
    global pool_list
    global new_load_at_hosts
    global new_load_at_hosts2
    pool_list = sorted(pool_list.items(), key=lambda item: item[1])
    pool_list = dict(pool_list)
    for i in pool_list:
        if pool_list[i] <= lower_threshold:
            list_of_services_to_be_killed = new_load_at_hosts2[i]
            for each_service in list_of_services_to_be_killed:
                entries = new_load_at_hosts[each_service]
                if len(entries)>1:#matlab dusri ip pe chal raha hai koi toh instance
                    service_entries = new_load_at_hosts2[i][each_service]
                    process_ids = [x[0] for x in service_entries]
                    instance_ids = [x[1] for x in service_entries]
                    k = 0
                    for process_id in process_ids:
                        request_MT = {"Request_Type": "Kill","IP" : i,"PID" : process_id,"Service_ID" : each_service,"Instance_ID":instance_ids[k]}
                        msg_obj.send("","modules_SM",request_MT)
                        k += 1
                else:
                    request_MT = {"Request_Type": "Service_Submit","Service_ID" : each_service,"Instances" : 1}
                    msg_obj.send("","LBB_HM",request_MT)
                    service_entries = new_load_at_hosts2[i][each_service]
                    process_ids = [x[0] for x in service_entries]
                    instance_ids = [x[1] for x in service_entries]
                    k = 0
                    for process_id in process_ids:
                        request_MT = {"Request_Type": "Kill","IP" : i,"PID" : process_id,"Service_ID" : each_service,"Instance_ID":instance_ids[k]}
                        msg_obj.send("","modules_SM",request_MT)
                        k += 1
            pool[i] = "available"

def service_downscaling():
    global service_ids
    global new_load_at_hosts
    global pool_list
    for service_id in service_ids:
        queue_name = "PlatformInputStream_"+service_id
        length_of_queue = msg_obj.queue_length('',queue_name)
        if length_of_queue <= lower_queue_threshold:
            no_of_ips = new_load_at_hosts[service_id]
            if len(no_of_ips) == 1:
                for ip in no_of_ips:
                    entries = new_load_at_hosts[service_id][ip]
                    instance_ids = [x[1] for x in entries]
                    no_of_instances = len(set(instance_ids))
                    if no_of_instances == 1:
                        return
                    else:
                        process_id,instance_id = entries[0]
                        request_MT = {"Request_Type": "Kill","IP" : ip,"PID" : process_id,"Service_ID" : service_id,"Instance_ID":instance_id}
                        msg_obj.send("","modules_SM",request_MT)
                        return
            else:
                ip1 = None
                load1 = 0
                for ip in no_of_ips:
                    load = pool_list[ip]
                    if load > load1:
                        ip1 = ip
                        load1 = load
                entries = new_load_at_hosts[service_id][ip1]
                process_id,instance_id = entries[0]
                request_MT = {"Request_Type": "Kill","IP" : ip,"PID" : process_id,"Service_ID" : service_id,"Instance_ID":instance_id}
                # request_MT = json.dumps(request_MT)
                msg_obj.send("","modules_SM",request_MT)
                return


if __name__ == '__main__':

    msg_obj.create_ServiceQueues("LB", "HM")
    # msg_obj.create_queue('',"LBHC_RG")
    # msg_obj.create_queue('',"RG_LBHC")
    # msg_obj.create_queue('',"LBSI_RG")
    # msg_obj.create_queue('',"RG_LBSI")
    msg_obj.create_queue('',"LB_SM")

    t_hm = Thread(target=Recieve_from_HM)
    t_hm.start()

    # t_hms = Thread(target=Recieve_from_HMS)
    # t_hms.start()
    #
    # t_hmm = Thread(target=Recieve_from_HMM)
    # t_hmm.start()

    t_rg_si = Thread(target=Recieve_from_RG_SI)
    t_rg_si.start()

    t_rg_hc = Thread(target=Recieve_from_RG_HC)
    t_rg_hc.start()

    getting_host_credentials()
    # reload_interval()
