$(function(){
		// Accordion
		$("#accordion").accordion({ header: "h3" });
		
		//Tabs
		$('#tabs').tabs();
		
		//Call Table Sorter
		$("#metaTable0").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#metaTable1").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#metaTable2").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#historyTable0").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#historyTable1").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#onAirTable").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#aliveTable").tablesorter({
			widgets: ['zebra']
		});
		
		//Call Table Sorter
		$("#poolTable").tablesorter({
			widgets: ['zebra']
		});
		
});

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

