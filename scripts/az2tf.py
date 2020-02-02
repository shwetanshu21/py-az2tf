#!/usr/bin/python
# RUNBOOK ON
import subprocess
import requests
import adal
import os
import json
import sys
import glob
import argparse
import ast
# RUNBOOK OFF
scwd=os.getcwd()
#print scwd
head, tail = os.path.split(scwd)
os.chdir(head)
cwd=os.getcwd()
head, tail = os.path.split(cwd)
newd=head+"/scripts"
# chdir scripts
os.chdir(newd)
#print os.getcwd()
#import azure_resources
# RUNBOOK ON
# RUNBOOK INLINE1
import azurerm_resource_group   # v12
import azurerm_management_lock  # v12
import azurerm_user_assigned_identity
import azurerm_availability_set    # v12
import azurerm_route_table    #v12 
import azurerm_application_security_group
import azurerm_network_security_group #v12
import azurerm_virtual_network    #v12
import azurerm_subnet    #v12
import azurerm_virtual_network_peering  #v12
import azurerm_managed_disk #v12
import azurerm_storage_account #v12
import azurerm_key_vault #v12
import azurerm_public_ip   #v12
import azurerm_traffic_manager_profile
import azurerm_traffic_manager_endpoint
import azurerm_network_interface  #v12
import azurerm_dns_zone
import azurerm_lb   #v12
import azurerm_lb_nat_rule  #v12
import azurerm_lb_nat_pool  #v12
import azurerm_lb_backend_address_pool  #v12
import azurerm_lb_probe  #v12
import azurerm_lb_rule  #v12
import azurerm_application_gateway

import azurerm_local_network_gateway
import azurerm_virtual_network_gateway    #v12
import azurerm_virtual_network_gateway_connection # --   #v12
import azurerm_express_route_circuit 
import azurerm_express_route_circuit_authorization
import azurerm_express_route_circuit_peering  # --
import azurerm_container_registry  #v12
import azurerm_kubernetes_cluster
import azurerm_recovery_services_vault #v12
import azurerm_virtual_machine  #v12
import azurerm_virtual_machine_extension  #v12
import azurerm_virtual_machine_scale_set #v12

import azurerm_automation_account  #v12
import azurerm_log_analytics_workspace  #v12
import azurerm_log_analytics_solution   #v12
import azurerm_image  # v12
import azurerm_shared_image_gallery  # v12
import azurerm_shared_image  # v12
import azurerm_shared_image_version  # v12
import azurerm_snapshot  # v12
import azurerm_network_watcher  # v12
import azurerm_cosmosdb_account
import azurerm_servicebus_namespace
import azurerm_servicebus_queue
import azurerm_eventhub_namespace
import azurerm_eventhub
import azurerm_eventhub_namespace_authorization_rule

import azurerm_sql_server
import azurerm_sql_database
import azurerm_databricks_workspace
import azurerm_app_service_plan
import azurerm_app_service
import azurerm_app_service_slot
import azurerm_function_app
import azurerm_logic_app_workflow
import azurerm_logic_app_trigger_http_request
import azurerm_monitor_autoscale_setting
import azurerm_api_management

import azurerm_policy_definition
import azurerm_policy_set_definition
import azurerm_policy_assignment
import azurerm_role_definition
import azurerm_role_assignment
# RUNBOOK OFF
os.chdir(scwd)
#print os.getcwd()

parser = argparse.ArgumentParser(description='terraform sub rg')
parser.add_argument('-c', help='Cloud')
parser.add_argument('-s', help='Subscription Id')
parser.add_argument('-g', help='Resource Group')
parser.add_argument('-r', help='Filter azurerm resource')
parser.add_argument('-p', help='Subscription Policies & RBAC')
parser.add_argument('-f', help='Fast Forward')
parser.add_argument('-d', help='Debug')
args = parser.parse_args()
ccld=args.c
csub=args.s
crg=args.g
crf=args.r
deb=args.d
pol=args.p
ff=args.f
    

cde=False
az2tfmess="# File generated by py-az2tf see: https://github.com/andyt530/py-az2tf \n"

if ccld is not None:
    if ccld == 'AzureCloud':
        cldurl='management.azure.com'
    elif ccld == 'AzureChinaCloud':
        cldurl='management.chinacloudapi.cn'
    elif ccld == 'AzureUSGovernment':
        cldurl='management.usgovcloudapi.net'
    elif ccld == 'AzureGermanCloud':
        cldurl='management.microsoftazure.de'
    else:
        cldurl='management.azure.com'
    print("Cloud=" + ccld)

# RUNBOOK OFF
if csub is not None:
   
    # validate sub
    if len(csub) != 36:
        print ("Expected subscription id to be 36 characters long got " + str(len(csub)) + " characters in " + csub)
        exit("Error: SubLength")


if crg is not None:
    print("resource group=" + crg)
    # validate rg
if pol is not None:
    print("Policies & RBAC=" + pol)
    # validate resource
if crf is not None:
    print("resource filter=" + crf)
    # validate resource
if deb is not None:
    cde=True
    print("Debug=" + str(cde))

if sys.version_info[0] < 3:
    #raise Exception("Must be using Python 2")
    print("Python version ", sys.version_info[0], " version 3 required, Exiting")
    exit()

def printf(format, *values):
    print(format % values )

# cleanup files with Python
#tffile=tfp+"*.tf"
#fileList = glob.glob(tffile) 
# Iterate over the list of filepaths & remove each file.
#for filePath in fileList:
#    try:
#        os.remove(filePath)
#    except:
#        print("Error while deleting file : ", filePath)


#with open(filename, 'w') as f:
    #print >> f, 'Filename:'


#tenant = os.environ['TENANT']
#authority_url = 'https://login.microsoftonline.com/' + tenant
#client_id = os.environ['CLIENTID']
#client_secret = os.environ['CLIENTSECRET']
#resource = 'https://management.azure.com/'
#context = adal.AuthenticationContext(authority_url)
#token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
#headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
#params = {'api-version': '2016-06-01'}
#url = 'https://management.azure.com/' + 'subscriptions'
#r = requests.get(url, headers=headers, params=params)
#print(json.dumps(r.json(), indent=4, separators=(',', ': ')))

print ("Get Access Token from CLI")
p = subprocess.Popen('az account get-access-token -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
c=0
for rline in p.stdout.readlines():
   
    line=str(rline)[5:]
    #line=line[5:]
    #print("---",line)
    if "accessToken" in line:
        #tk=line.split(":")[1]
        tk=line.split('"')[2]
        #print("tk=",tk)
        tk2=tk.replace(",", "")
        bt2=tk2.replace('"', '')
    if "subscription" in line:
        try:
            tk=line.split(":")[1].strip(' ",')
        except IndexError:
            print("Error getting subscription - Login again with CLI\n")
            exit("LoginWithCli")

        tk2=tk.replace(",", "")
        sub2=tk2.replace('"', '')
retval = p.wait()
if csub is not None:
    sub=csub
else:
    sub=sub2.rstrip('\n')

#bt=bt2.rstrip('\n')
bt=bt2.rstrip()
print ("Subscription:",sub)
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}
# print "CloudURL:",cldurl
# print "BearerToken:",bt

# subscription check

url="https://" + cldurl + "/subscriptions/"
#print("url=",url)
#print("headers=",headers)
params = {'api-version': '2014-04-01'}
try: 
    r = requests.get(url, headers=headers, params=params)
    print(str(r))
    subs = r.json()["value"]
except KeyError:
    print ("Error getting subscription list")
    exit("ErrorGettingSubscriptionList")
#print(json.dumps(subs, indent=4, separators=(',', ': ')))
#ssubs=json.dumps(subs)
#print ssubs
#if sub not in ssubs: 
#    print "Could not find subscription with ID " + sub + " Exiting ..." 
#    exit("ErrorInvalidSubscriptionID-1")


#print(json.dumps(subs, indent=4, separators=(',', ': ')))

FoundSub=False
count=len(subs)

for i in range(0, count):
    id=str(subs[i]["subscriptionId"])
    #print id + " " + sub
    if id == sub:
        FoundSub=True

#if not FoundSub:
#    print "Could not find subscription with ID " + sub + " Exiting ..." 
    #exit("Error: InvalidSubscriptionID-2")

print ("Found subscription " + sub + " proceeding ...")

if crg is not None:
    FoundRg=False
    # get and check Resource group
    url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups"
    params = {'api-version': '2014-04-01'}
    r = requests.get(url, headers=headers, params=params)
    rgs= r.json()["value"]

    count=len(rgs)
    for j in range(0, count):    
        name=rgs[j]["name"]
        if crg.lower() == name.lower():
            print ("Found Resource Group" + crg)
            FoundRg=True

    if not FoundRg:
        print ("Could not find Resource Group " + crg + " in subscription " + sub + " Exiting ...")
        exit("ErrorInvalidResourceGroup")


if os.path.exists("tf-staterm.sh"):
    os.remove('tf-staterm.sh')
if os.path.exists("tf-stateimp.sh"):
    os.remove('tf-stateimp.sh')


if crf is None: crf="azurerm"


if pol is not None:
 
    azurerm_policy_definition.azurerm_policy_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
    azurerm_policy_assignment.azurerm_policy_assignment(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
    azurerm_policy_set_definition.azurerm_policy_set_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
    azurerm_role_definition.azurerm_role_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
    azurerm_role_assignment.azurerm_role_assignment(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
    


# RUNBOOK ON
# RUNBOOK INLINE2

# record and sort resources - no longer needed
# azure_resources.azure_resources(crf,cde,crg,headers,requests,sub,json,az2tfmess,os)
# 001 Resource Group
azurerm_resource_group.azurerm_resource_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 002 management lock
azurerm_management_lock.azurerm_management_lock(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 015 user assigned identity
azurerm_user_assigned_identity.azurerm_user_assigned_identity(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 020 Avail Sets
azurerm_availability_set.azurerm_availability_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 030 Route Table
azurerm_route_table.azurerm_route_table(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 040 ASG
azurerm_application_security_group.azurerm_application_security_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 050 NSG's
azurerm_network_security_group.azurerm_network_security_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 060 Virtual Networks
azurerm_virtual_network.azurerm_virtual_network(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 070 subnets
azurerm_subnet.azurerm_subnet(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 080 vnet peering
azurerm_virtual_network_peering.azurerm_virtual_network_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 090 Key Vault - using cli
azurerm_key_vault.azurerm_key_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 100 managed disk
azurerm_managed_disk.azurerm_managed_disk(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 110 storgae account
azurerm_storage_account.azurerm_storage_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 120 public ip
azurerm_public_ip.azurerm_public_ip(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 124 Traffic manager profile
azurerm_traffic_manager_profile.azurerm_traffic_manager_profile(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 125 traffic manager endpoint
azurerm_traffic_manager_endpoint.azurerm_traffic_manager_endpoint(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 130 network interface
azurerm_network_interface.azurerm_network_interface(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 131_azurerm_dns_zone
azurerm_dns_zone.azurerm_dns_zone(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 140_azurerm_lb
azurerm_lb.azurerm_lb(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 150_azurerm_lb_nat_rule
azurerm_lb_nat_rule.azurerm_lb_nat_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 160_azurerm_lb_nat_pool
azurerm_lb_nat_pool.azurerm_lb_nat_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 170_azurerm_lb_backend_address_pool
azurerm_lb_backend_address_pool.azurerm_lb_backend_address_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 180_azurerm_lb_probe
azurerm_lb_probe.azurerm_lb_probe(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 190_azurerm_lb_rule
azurerm_lb_rule.azurerm_lb_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 193_azurerm_application_gateway
azurerm_application_gateway.azurerm_application_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 200_azurerm_local_network_gateway
azurerm_local_network_gateway.azurerm_local_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 210_azurerm_virtual_network_gateway
azurerm_virtual_network_gateway.azurerm_virtual_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 220_azurerm_virtual_network_gateway_connection
azurerm_virtual_network_gateway_connection.azurerm_virtual_network_gateway_connection(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 230_azurerm_express_route_circuit
azurerm_express_route_circuit.azurerm_express_route_circuit(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 240_azurerm_express_route_circuit_authorization
azurerm_express_route_circuit_authorization.azurerm_express_route_circuit_authorization(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 250_azurerm_express_route_circuit_peering
azurerm_express_route_circuit_peering.azurerm_express_route_circuit_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 260_azurerm_container_registry
azurerm_container_registry.azurerm_container_registry(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 270_azurerm_kubernetes_cluster
azurerm_kubernetes_cluster.azurerm_kubernetes_cluster(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 280_azurerm_recovery_services_vault
azurerm_recovery_services_vault.azurerm_recovery_services_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 290_azurerm_virtual_machine
azurerm_virtual_machine.azurerm_virtual_machine(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 290_azurerm_virtual_machine_extension
azurerm_virtual_machine_extension.azurerm_virtual_machine_extension(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 295_azurerm_virtual_machine_scale_set
azurerm_virtual_machine_scale_set.azurerm_virtual_machine_scale_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 310_azurerm_automation_account
azurerm_automation_account.azurerm_automation_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 320_azurerm_log_analytics_workspace
azurerm_log_analytics_workspace.azurerm_log_analytics_workspace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 330_azurerm_log_analytics_solution
azurerm_log_analytics_solution.azurerm_log_analytics_solution(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 340_azurerm_image
azurerm_image.azurerm_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 341_azurerm_shared_image_gallery
azurerm_shared_image_gallery.azurerm_shared_image_gallery(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
azurerm_shared_image.azurerm_shared_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
azurerm_shared_image_version.azurerm_shared_image_version(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 350_azurerm_snapshot
azurerm_snapshot.azurerm_snapshot(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 360_azurerm_network_watcher
azurerm_network_watcher.azurerm_network_watcher(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 400_azurerm_cosmosdb_account
azurerm_cosmosdb_account.azurerm_cosmosdb_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 500_azurerm_servicebus_namespace
azurerm_servicebus_namespace.azurerm_servicebus_namespace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 510_azurerm_servicebus_queue
azurerm_servicebus_queue.azurerm_servicebus_queue(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 520_azurerm_eventhub_namespace
azurerm_eventhub_namespace.azurerm_eventhub_namespace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 521_azurerm_eventhub
azurerm_eventhub.azurerm_eventhub(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 522_azurerm_eventhub_namespace_authorization_rule
azurerm_eventhub_namespace_authorization_rule.azurerm_eventhub_namespace_authorization_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 540_azurerm_sql_server
azurerm_sql_server.azurerm_sql_server(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 541_azurerm_sql_database
azurerm_sql_database.azurerm_sql_database(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
if ccld != 'AzureChinaCloud':
# 550_azurerm_databricks_workspace
    azurerm_databricks_workspace.azurerm_databricks_workspace(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 600_azurerm_app_service_plan
azurerm_app_service_plan.azurerm_app_service_plan(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 610_azurerm_app_service
azurerm_app_service.azurerm_app_service(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 611_azurerm_app_service_slot
azurerm_app_service_slot.azurerm_app_service_slot(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)
# 620_azurerm_function_app
azurerm_function_app.azurerm_function_app(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 630_azurerm_logic_app_workflow
azurerm_logic_app_workflow.azurerm_logic_app_workflow(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)


# 640_azurerm_api_management
azurerm_api_management.azurerm_api_management(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# 631_azurerm_logic_app_trigger_http_request
# AWAITING terraform import fix
#azurerm_logic_app_trigger_http_request.azurerm_logic_app_trigger_http_request(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

if ccld != 'AzureChinaCloud':
# 650_azurerm_monitor_autoscale_setting
    azurerm_monitor_autoscale_setting.azurerm_monitor_autoscale_setting(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl)

# ******************************************************************************************
# RUNBOOK OFF
exit()



