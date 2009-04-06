function GetHostStatus()
{
	var hostlist = document.getElementById("HostList");
	var myhost = hostlist.options[hostlist.selectedIndex].text;
	if (myhost == "----------")
	{
		window.location="/washtub/";
	}
	else
	{
		window.location="/washtub/status/"+myhost;
	}
}

function PostQueueRequest(uri)
{
	var request_list = document.getElementById("uriInstance");
	var request = request_list.options[request_list.selectedIndex].text;
	
	var hostlist = document.getElementById("HostList");
	var myhost = hostlist.options[hostlist.selectedIndex].text;
	
	window.location="/washtub/queue/push/"+myhost+"/"+request+"&uri="+uri;
} 

