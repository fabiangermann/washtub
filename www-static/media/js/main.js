
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
		window.location="/washtub/control/"+myhost;
	}
} 

