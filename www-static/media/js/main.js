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

var timeout = 750; // Effects and general UI response timeouts
var refresh_timeout = 0; // This is the trigger to use on clearInterval

function setupUI() {
  // Start the countdown until the next track
  refresh_timeout = countdownRefresh();

  //Tabs
  $('#tabs').tabs({ cookie: { path: baseurl, name: "washtub-tabs" },
                    ajaxOptions: { cache: false },
                    spinner: "" //'<img width="50%" height="50%" src="{{ "media/images/throbber.gif"|baseurl }}"></img>'
  });
  $('#tabs').bind('tabsload', function(event, ui) {
    //console.log("In tabsload: " + window.location.hash);
    var index = $('#tabs').tabs( "option", "selected" );
    
    // Do these actions for all tabs
    // Stripe the Tablesorters
    $.tablesorter.defaults.widgets = ['zebra'];

    // Stripe the rest of the tables
    $('tr:nth-child(even)').addClass("odd");

    // Status Tab
    if (index == '0') {
      $.history.load('status');
      $("#aliveTable").tablesorter();
      $("#onAirTable").tablesorter();
      $('button#skip').button({
        icons: {
          primary: "ui-icon-seek-end"
        },
        text: false
      });
      $('button#play').button({
        icons: {
          primary: "ui-icon-play"
        },
        text: false
      });
      $('button#stop').button({
        icons: {
          primary: "ui-icon-stop"
        },
        text: false
      });
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
      //console.log("In tabsload, pool tab: " + hash);
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
  $("button#refresh").button({
    icons: {
      primary: "ui-icon-arrowrefresh-1-e",
    },
    text: false,
  });
  $("button#refresh").click(
    function() {
      clearInterval(refresh_timeout);
      refreshStatus(0);
      refreshTab(0);
    }
  );
  $('button#edit-metadata').button({
    icons: {
      primary: "ui-icon-pencil"
    },
    text: false
  });
  $('button#edit-metadata').click(function() {
    $('#dialog-edit-metadata').dialog('open');
  });
  
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

  // Dialog Edit Metadata
  $('#dialog-edit-metadata').dialog({
    autoOpen: false,
    width: 350,
    buttons: {
      "Update": function() {
        insertMetadata($('#dialog-edit-metadata form'));
        $(this).dialog("close");
        // Trigger the request to washtub for metdata update
      },
      "Cancel": function() {
        $(this).dialog("close");
      }
    }
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
        refreshTab(timeout*2);
      },
      error: function(jqXHR, textStatus)  {
        Pnotify("error", "Queue reorder failed: " + textStatus);
        // Reload the current tab
        refreshTab(0);
      },
    });
  }
  else {
    $(table_row_id).effect("highlight", { color: red }, timeout);
    Pnotify("error", "Queue operation failed: Items cannot be moved to the last position.");

    // Reload the current tab
    refreshTab(timeout*2);
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
        refreshStatus(timeout);
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
    refreshTab(timeout);
}

function streamControl(form, action, stream) {
    var token = form.csrfmiddlewaretoken.value;
    var url = baseurl + "control/" + action + "/" + host + "/" + stream;
    $.ajax({
      type: "POST",
      url: url,
      sync: false,
      data: { 'csrfmiddlewaretoken': token},
      dataType: "json",
      success: function(data){
        var notify_type = 'notice';
        var base_msg = "Stream " + action + " " + stream + " : ";
        var status_color = green;
        if (data.type == 'error') {
          notify_type = data.type;
          status_color = red;
        }
        Pnotify(notify_type, base_msg + data.msg);
        $(form.button).effect("highlight", { color: status_color }, timeout);
      },
      error: function(jqXHR, textStatus)  {
        Pnotify("error", "Stream '" + stream + "' skip failed: " + textStatus);
        $(form.remove).effect("highlight", { color: red }, timeout);
      },
    });
    // Reload the current tab
    refreshTab(timeout);
    refreshStatus(timeout*2);
    return false;
}

function insertMetadata(dialog_form) {
    var query_string = $(dialog_form).serialize();
    var url = baseurl + "control/metadata/" + host;
    $.ajax({
      type: "POST",
      url: url,
      sync: false,
      data: query_string,
      dataType: "json",
      success: function(data){
        var notify_type = 'notice';
        var base_msg = "Insert metadata: ";
        var status_color = green;
        if (data.type == 'error') {
          notify_type = data.type;
          status_color = red;
        }
        Pnotify(notify_type, base_msg + data.msg);
      },
      error: function(jqXHR, textStatus)  {
        Pnotify("error", "Insert metadata failed: " + textStatus);
      },
    });
    // Reload the current tab
    refreshTab(timeout);
    refreshStatus(timeout*2);
    return false;
}

/* Function to perform a new search, usually clicked from related info
   links in the pool and search pages */
function Search(term, type, pg_num) {
  var search = '';
  var tab = 2;
  var current_url = '';
  var count = 0;
  // Check what url we have loaded in the current tab
  $('#tabs > ul li a').each(function() {
    if (count == tab) {
      current_url = $(this).data('load.tabs');
    }
    count++;
  });

  var hash = ['search', type, pg_num];
  if (term != undefined && term != '') {
    hash.push(term);
    search = '&search=' + term;
  }
  // XXX: We need to enable search types for type: album, artist, song
  var search_url = baseurl + 'pool/search/' + host + '/'+ pg_num + '?type=song' + search;
  if ( search_url == current_url ) {
    //console.log('In Search() and doing nothing.  I suspect this url has already been loaded');
    return false;
  }

  //console.log('In Search(), current hash: ' + window.location.hash + ', new hash: #' + hash.join('-'));
  $('#tabs').tabs('url', tab, search_url);
  $('#tabs').tabs('select', tab);
  $('#tabs').tabs('load', tab);
  $('#tabs').tabs('show', tab);
  return false;
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

function toMinutes(seconds) {
  var minutes = parseInt((seconds / 60));
  var seconds = '' + parseInt((seconds % 60));
  if (seconds.length == 1) {
    seconds = '0' + seconds;
  }
  return minutes + ':' + seconds;
}

/* Function to facilitate auto refresh on track changes
   This takes no arguments, but could probably use some
   inputs to specify the refresh function
*/   
function countdownRefresh() {
  var empty = '--:--';
  var get_value = $("div#remaining.status-info");
  var count = parseInt($(get_value).html());
  //alert(count); 
  countdown = setInterval(function(){
    //var start = new Date()
    //start = start.getTime() + (start.getMilliseconds()/1000);
    var status_display = $("div.status-remaining");
    var node_display = $("td.remaining");
    if ( isNaN(count) || count < 0) {
      $(status_display).html(empty);
      $(node_display).html(empty);
      clearInterval(refresh_timeout);
    }
    else if ( count == 0 ) {
      $(status_display).html(empty);
      $(node_display).html(empty);
      clearInterval(refresh_timeout);
      // Refresh again, but be sure to give
      // liquidsoap time for next track load
      refreshStatus(timeout*5);
      refreshTab(timeout*5);
    }
    else {
      $(status_display).html(toMinutes(count));
      $(node_display).html(toMinutes(count));
      if ( (count % 30) == 0 ) {
        refreshStatus(timeout);
        if ( $("#tabs").tabs("option","selected") == 0 ) { 
          refreshTab(timeout); // Only refresh the status tab here
        }
      }
    }
    count--;
    //var now = new Date();
    //now = now.getTime() + (now.getMilliseconds()/1000);
    ////console.log("In countdownRefresh(): time to execute: now (" + now + ") - start(" + start + ") = " + (now - start));
  }, 1000);
  return countdown;
}

/* Function to refresh status of the page.  This will reload
   the current tab as well as refresh status info in the header
   section for artist, title, etc
*/

function refreshStatus(delay) {
  //console.log('In refreshStatus: host=' + host);
  if ( host == '' || host == undefined ) {
    return;
  }

  // Then move on to the status header section
  var url = baseurl + "status/" + host; 
  var props = { 'now_playing': ['title', 'artist', 'album', 'genre', 'remaining', 'tracknumber', 'year'],
                'status' : ['remaining', 'uptime']
  };

  // Setup a variable to grab for the status timeout
  var remaining = 0;

  setTimeout(function() {
    $.ajax({
        type: "GET",
        url: url + '?',
        sync: false,
        dataType: "json",
        success: function(data){
          for ( var key in props) {
            // FLAC has to be difficult and use 'date' instead of 'year'
            if (data[key].hasOwnProperty('decoder') && data[key]['decoder'] == 'FLAC') {
              //console.log("In refreshStatus: decoder is FLAC");
              var decoder = 'FLAC';
            }
            // Check to see if the key existed in the response
            if (data.hasOwnProperty(key)) {
              var s = data[key];
              for (i=0; i < props[key].length; i++) {
                var label = props[key][i];
                var element = $('div#' + label + '.status-info');
                var meta_form = $('input#' + label + '.status-info');
                var text = '';

                // The html label above is still 'year', but the data itself will be 'date' for FLAC
                if (label == 'year' && decoder == 'FLAC') {
                  label = 'date';
                }
                if (s.hasOwnProperty(label)) {
                  text = s[label];
                  if ( label == 'remaining' ) {
                    remaining = text
                  }
                }
                // Set the text even if it's empty. We dont want old metadata to persist.
                $(element).html(text);
                $(meta_form).val(text);
              }
            }
         }
         // If we were successful, let's restart the timer
         // And also clear the existing timer, just in case
         // But only if there's actually something playing
         if ( remaining > 0 ) {
           clearInterval(refresh_timeout); 
           refresh_timeout = countdownRefresh();
         }
       },
       error: function(jqXHR, textStatus)  {
         Pnotify("error", "Status update failed: " + textStatus);
       },
    });
  }, delay);  
}

function refreshTab(delay) {
   // Reload the current tab first
  var current_index = $("#tabs").tabs("option","selected");
  setTimeout(function() {
      $("#tabs").tabs("load", current_index);
    },
    delay
  );
}
