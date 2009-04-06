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

function PostQueueRequest()
{
	var uri_list = document.getElementById("uriInstance");
	var uri = uri_list.options[uri_list.selectedIndex].text;
	
	var hostlist = document.getElementById("HostList");
	var myhost = hostlist.options[hostlist.selectedIndex].text;
	
	window.location="/washtub/queue/push/"+myhost+"&uri="+uri;
} 

