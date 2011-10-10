/*
    Copyright (c) 2009, Chris Everest
    This file is part of Washtub.

    Washtub is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Washtub is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Washtub.  If not, see <http://www.gnu.org/licenses/>.
*/

/*  Add Custom Javascript Here */

/* Initial JQuery UI setup */
function setupUI() {
  //Tabs
  $('#tabs').tabs({ cookie: { path: baseurl, name: "washtub-tabs" },
                    ajaxOptions: { cache: false },
                    spinner: "" //'<img width="50%" height="50%" src="{{ "media/images/throbber.gif"|baseurl }}"></img>'
  });
  $('#tabs').bind('tabsload', function(event, ui) {
    // Stripe the Tablesorters
    $.tablesorter.defaults.widgets = ['zebra'];

    // Stripe the rest of the tables
    $('tr:nth-child(even)').addClass("odd");

    // Call Table Sorter
    // This is hackish, but zebra widgets don't refresh automagically after
    // ajax responses in tables
    // A better solution would be to check the active tab and only instantiate
    //  the tablesorters that we need (speed enhancement)
    $("#aliveTable").tablesorter();
    $("#onAirTable").tablesorter();
    $("#historyTable0").tablesorter();
    $("#historyTable1").tablesorter();
    $("#poolTable").tablesorter();
    $('#EqueueTable').tableDnD({
      onDrop: function(table, row) {
        if (host != '') {
          QueueReorder(table, row, host, baseurl);
        }
      }
    });
    $('button#remove').button({
      icons: {
        primary: "ui-icon-close"
      },
      text: false
    });
    $('button#info').button({
      icons: {
        primary: "ui-icon-info"
      },
      text: false
    });
    $('button#info').tooltip({
      events: {def: "'click','mouseleave'"},
      position: "top left",
      offset: [15, -60],
      predelay: 25,
      //delay: 0,
      //opacity: 0.75,
 });
  });

  $('button').button();
  $("button#refresh").click(
    function() {
      var current_index = $("#tabs").tabs("option","selected");
      $("#tabs").tabs("load", current_index);
    }
  );
  
  // Dialog
  $('#dialog_scan').dialog({
    autoOpen: false,
    width: 350,
    buttons: {
      "OK": function() {
        $(this).dialog("close");
        window.location=filescanner_url;
      },
      "Cancel": function() {
        $(this).dialog("close");
      }
    }
  });

  // Dialog Link
  $('#dialog_scan_link').click(function(){
    $('#dialog_scan').dialog('open');
      return false;
  });
}

/* Function used to determine and select the active host */
function GetHostStatus() {
	var hostlist = document.getElementById("HostList");
        var myhost = hostlist.options[hostlist.selectedIndex].text;
        if (myhost == "----------")
        {
                window.location=base_url;
        }
        else
        {
                window.location=baseurl + "status/" + myhost;
        }
}

/* Default Pnotify call */
function Pnotify(type, msg) {
        if(type != 'error' && type != 'notice') {
                return;
        }
        $.pnotify({
                pnotify_title: false,
                pnotify_text: msg,
                pnotify_type: type,
                pnotify_hide: true,
                pnotify_delay: 2500,
                pnotify_history: false,
                pnotify_addclass: "stack-queues",
                //pnotify_notice_icon: '',
                //pnotify_opacity: .85,
                //pnotify_nonblock: true,
                //pnotify_nonblock_opacity: .75
        });
}

/* Function to manipulate the queue depending on the active
/  host.  Called from TableDnD
*/
function QueueReorder(table, row, host, base_url) {
  var offset;
  var rid;
  var pos;
  var max;
  var row_id = '#'+row.id;
  var table_row_id = '#'+table.id+' '+row_id;
  var queue = table.tBodies[0].id;
  for (var i=0; i<table.rows.length; i++) {
    if (table.rows[i].id == row.id) {
      rid = table.rows[i].getElementsByClassName('rid')[0].innerHTML;
      // Offset is determined by liquidsoap and depends on whether a track
      // in the queue is actually live and playing. We then subtract an
      // additional unit from the offset to make up for the table header
      offset = table.rows[i].getElementsByClassName('offset')[0].innerHTML;
      pos = (i - offset) - 1;
    }
    max = (i - offset) - 1;
  }
  if ( pos != max && pos != row.id) {
    var url = base_url + "queue/move/" + host;
    $.ajax({
      type: "GET",
      url: url,
      sync: false,
      data: { 'queue': queue, 'rid': rid, 'pos': pos},
      dataType: "json",
      success: function(data){
        var notify_type = 'notice';
        var status_color = green;
        var base_msg = 'Queue reorder: ';
        if (data.type == 'error') {
          status_color = red; // shade of red
          notify_type = data.type;
        }
        Pnotify(notify_type, base_msg + data.msg);
        //alert("Server Response: '" + data.msg + "'\n\nQueue: " + queue + "\nOrig Row: "+ row_id + "\nRID is: " + rid + "\nNew Position: " + pos );
        $(table_row_id).effect("highlight", { color: status_color }, timeout);

        // Reload the current tab
        var current_index = $("#tabs").tabs("option","selected");
        setTimeout(function() { $("#tabs").tabs("load", current_index); }, timeout)
      },
      error: function(jqXHR, textStatus)  {
        Pnotify("error", "Queue reorder failed: " + textStatus);
        // Reload the current tab
        var current_index = $("#tabs").tabs("option","selected");
        setTimeout(function() { $("#tabs").tabs("load", current_index); }, timeout);
      },
    });
  }
  else {
    $(table_row_id).effect("highlight", { color: red }, timeout);
    Pnotify("error", "Queue operation failed: Items cannot be moved to the last position.");

    // Reload the current tab
    var current_index = $("#tabs").tabs("option","selected");
    setTimeout(function() { $("#tabs").tabs("load", current_index); }, timeout);
  }
}

/* Function used to push new requests into the specified queue */
function QueuePush(form, uri, host, base_url) {
    var queue = form.queue.value;
    var token = form.csrfmiddlewaretoken.value;
    var url = base_url + "queue/push/" + host;
    //alert(queue + ' ' + uri + ' ' + token + ' ' + host + ' ' + url);
    $.ajax({
      type: "POST",
      url: url,
      sync: false,
      data: { 'queue': queue, 'song_uri': uri, 'csrfmiddlewaretoken': token},
      dataType: "json",
      success: function(data){
        var notify_type = 'notice';
        var base_msg = 'Queue push: ';
        var status_color = green;
        if (data.type == 'error') {
          notify_type = data.type;
          status_color = red;
        }
        Pnotify(notify_type, base_msg + data.msg);
        $(form.queue).effect("highlight", { color: status_color }, timeout);
      },
      error: function(jqXHR, textStatus)  {
        Pnotify("error", "Queue push failed: " + textStatus);
        $(form.queue).effect("highlight", { color: red }, timeout);
      },
    });
    setTimeout(function () {form.queue.selectedIndex = 0;}, timeout+10);
}

/* Function used to remove existing request from the specified queue */
function QueueRemove(form, queue, rid) {
    var token = form.csrfmiddlewaretoken.value;
    var url = baseurl + "queue/remove/" + host;
    //alert(queue + ' ' + uri + ' ' + token + ' ' + host + ' ' + url);
    $.ajax({
      type: "POST",
      url: url,
      sync: false,
      data: { 'queue': queue, 'rid': rid, 'csrfmiddlewaretoken': token},
      dataType: "json",
      success: function(data){
        var notify_type = 'notice';
        var base_msg = 'Queue remove: ';
        var status_color = green;
        if (data.type == 'error') {
          notify_type = data.type;
          status_color = red;
        }
        Pnotify(notify_type, base_msg + data.msg);
        $(form.button).effect("highlight", { color: status_color }, timeout);
      },
      error: function(jqXHR, textStatus)  {
        Pnotify("error", "Queue remove failed: " + textStatus);
        $(form.remove).effect("highlight", { color: red }, timeout);
      },
    });
    // Reload the current tab
    var current_index = $("#tabs").tabs("option","selected");
    setTimeout(function() { $("#tabs").tabs("load", current_index); }, timeout);
}

/* Function to perform a new search, usually clicked from related info
   links in the pool and search pages */
function Search(term, type, pg_num) {
  var search = '';
  if ( term != '') {
    search = '&search=' + term;
  }
  var search_url = baseurl + 'pool/search/' + host + '/'+ pg_num;
  var current_index = $("#tabs").tabs("option","selected");
  $('#tabs').tabs('url', current_index, search_url + '?type=song' + search);
  $('#tabs').tabs('load', current_index);
}
