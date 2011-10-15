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
    var index = $('#tabs').tabs( "option", "selected" );
    
    // Do these actions for all tabs
    // Stripe the Tablesorters
    $.tablesorter.defaults.widgets = ['zebra'];

    // Stripe the rest of the tables
    $('tr:nth-child(even)').addClass("odd");

    // Status Tab
    if (index == '0') {
      //$.history.load('status');
      window.location.hash = '';
      $("#aliveTable").tablesorter();
      $("#onAirTable").tablesorter();
    }
    // Queue Tab
    if (index == '1') {
      $.history.load('queues');
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
    }
    // Pool Tab (and search)
    if (index == '2') {
      // Get the url
      var count = 0;
      var url = '';

      // Define a default hash value (no search crit defined)
      var hash = 'pool';

      // Get the current url that loads into pool tab
      $('#tabs > ul li a').each(function() {
        if (count == 2) {
          url = $(this).data('load.tabs');
        }
        count++;
      });

      // Parse the url params (that define search crit)
      var params = UrlParams(url);

      // Build the hash value on the search crit
      if ('type' in params) {
        hash = 'search-' + params['type'];
        if ('pg' in params) {
          hash += '-' + params['pg'];
        } else {
          hash = '-1';
        }
        if ('search' in params) {
          hash += '-' + params['search'];
        }
      }
      $.history.load(hash);
      
      // Finish loading the rest of the tab elements
      $("#poolTable").tablesorter();
      $('button#info').button({
        icons: {
          primary: "ui-icon-info"
        },
        text: false
      });
      $('button#info').tooltip({
        //events: {def: "click,mouseout"},
        position: "top left",
        offset: [15, -60],
        predelay: 25,
        //delay: 0,
        //opacity: 0.75,
      });
    }
    // History Tab
    if (index == '3') { 
      $.history.load('history');
      $("#historyTable0").tablesorter();
      $("#historyTable1").tablesorter();
    }
    // Help Tab
    if (index == '4') {
      $.history.load('help');
      // Nothing here yet
    }
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
  var tab = '2';
  var hash = ['search', type, pg_num];
  if (term != undefined && term != '') {
    hash.push(term);
    search = '&search=' + term;
  }
  var search_url = baseurl + 'pool/search/' + host + '/'+ pg_num;
  var current_index = $("#tabs").tabs("option","selected");
  // XXX: We need to enable search types for type: album, artist, song
  $('#tabs').tabs('url', 2, search_url + '?type=song' + search);
  $('#tabs').tabs('select', tab);
  $('#tabs').tabs('load', tab);
  $('#tabs').tabs('show', tab);
}

/* Function to parse the url params out of a full url.
   We use this to determine what state a tab is in, using
   the url that is loaded.
*/

function UrlParams(s) {
    var params = {},
        e,
        a = /\+/g,  // Regex for replacing addition symbol with a space
        b = /(\d+)\?(.*)/,
        r = /([^&=]+)=?([^&]*)/g,
        d = function (s) { return decodeURIComponent(s.replace(a, " ")); };
    if(q = b.exec(s)) {
      params['pg']=q[1];
    }
    else { return params; }
    while (e = r.exec(q[2]))
       params[d(e[1])] = d(e[2]);
    return params;
}
