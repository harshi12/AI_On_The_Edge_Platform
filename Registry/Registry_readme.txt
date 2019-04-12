Types of JSON requests:

1. Write in data structure Service_inst_info with Value as Model_id with list of list [ ip , port with model, up or down]
{
	"Request_Type": "Write",
	"DS_Name": "Service_inst_info",
	"Value": [{
			"Model_id": 432,
			"Hosts": [
				["192.168.10.23", 6253, "Up"],
				["192.163.10.23", 6255, "Down"]
			]
		},
		{
			"Model_id": 482,
			"Hosts": [
				["192.168.10.27", 6298, "Up"],
				["192.163.10.25", 6267, "Down"]
			]
		}
	]

}

2. Read in data structure Service_inst_info
{
	"Request_Type": "Read",
	"DS_Name": "Service_inst_info",
  "Filter" : [{"Model_Id" : 432},{"Model_id" : 645}]
}

3. Write in data structure App_inst_info with Value as App_id with list of list [ ip , port with app, up or down]
{
	"Request_Type": "Write",
	"DS_Name": "App_inst_info",
	"Value": [{
			"App_id": 432,
			"Hosts": [
				["192.168.10.23", 6253, "Up"],
				["192.163.10.23", 6255, "Down"]
			]
		},
		{
			"App_id": 482,
			"Hosts": [
				["192.168.10.27", 6298, "Up"],
				["192.163.10.25", 6267, "Down"]
			]
		}
	]

}

4. Read in data structure App_inst_info
{
	"Request_Type": "Read",
	"DS_Name": "App_inst_info",
  "Filter" : [{"App_id" : 432}]
}

5. Write in data structure Storage_info with Value as App_id with dict of 3 links [Model_link, App_Link, Config_Link]
{
	"Request_Type": "Write",
	"DS_Name": "Storage_info",
	"Value": [
    {
			"App_id": 234,
			"Model_Link": "/AD_ID/App_ID/Model",
			"App_Link": "/AD_ID/App_ID/App",
			"Config_Link": "/AD_ID/App_ID/Config"
		},
		{
			"App_id": 245,
			"Model_Link": "192.168.12.11:7354/Model_Folder_Repo_Path",
			"App_Link": "192.168.12.11:7354/App_Folder_Repo_Path",
			"Config_Link": "192.168.12.11:7354/Config_Folder_Repo_Path"
		}
	]
}
6.  Read in data structure Storage_info
{
	"Request_Type": "Read",
	"DS_Name": "Storage_info",
  "Filter" : [{"App_id" : 432}]
}
