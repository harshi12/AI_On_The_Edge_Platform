Types of JSON requests:

1. Write in data structure Model_inst_info with Value as Model_id with list of list [ ip , port with model, up or down]
{
	"Request_Type": "Write",
	"DS_Name": "Model_inst_info",
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

2. Read in data structure Model_inst_info
{
	"Request_Type": "Read",
	"DS_Name": "Model_inst_info",
  "Filter" : {"Model_Id" : [432, 634]}
}

3. Write in data structure Service_inst_info with Value as Service_id with list of list [ ip , port with model, up or down]
{
	"Request_Type": "Write",
	"DS_Name": "Service_inst_info",
	"Value": [{
			"Service_id": 432,
			"Hosts": [
				["192.168.10.23", 6253, "Up"],
				["192.163.10.23", 6255, "Down"]
			]
		},
		{
			"Service_id": 482,
			"Hosts": [
				["192.168.10.27", 6298, "Up"],
				["192.163.10.25", 6267, "Down"]
			]
		}
	]

}

4. Read in data structure Service_inst_info
{
	"Request_Type": "Read",
	"DS_Name": "Service_inst_info",
  "Filter" : {"Service_Id" : [432,645]}
}

5. Write in data structure App_inst_info with Value as App_id with list of list [ ip , port with app, up or down]
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

6. Read in data structure App_inst_info
{
	"Request_Type": "Read",
	"DS_Name": "App_inst_info",
  "Filter" : {"App_id" : [432,745]}
}

7. Write in data structure Storage_info with Value as App_id with dict of 3 links [Model_link, App_Link, Config_Link]
{
	"Request_Type": "Write",
	"DS_Name": "Storage_info",
	"Value": [
    {
			"App_id": 234,
			"Model_Link": "/AD_ID/App_ID/Models",
			"App_Link": "/AD_ID/App_ID/AppLogic",
			"Service_Link": "/AD_ID/App_ID/Services",
			"Config_Link": "/AD_ID/App_ID/Config"
		},
		{
			"App_id": 244,
			"Model_Link": "/AD_ID/App_ID/Models",
			"App_Link": "/AD_ID/App_ID/AppLogic",
			"Service_Link": "/AD_ID/App_ID/Services",
			"Config_Link": "/AD_ID/App_ID/Config"
		}
	]
}

8.  Read in data structure Storage_info
{
	"Request_Type": "Read",
	"DS_Name": "Storage_info",
  "Filter" : {"App_id" : [432,543]}
}
