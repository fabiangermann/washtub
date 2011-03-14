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

/* Function to manipulate the queue depending on the active
/  host.  Called from TableDnD
*/
function QueueReorder(table, row, host, base_url) {
  var offset;
  var rid;
  var pos;
  var max;
  var timeout = 750; // timeout used for user feedback and page refresh
  var red = "#EE8A7C";
  var green = "#ABEE87";
  var row_id = '#'+row.id;
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
    $.get(url, { 'queue': queue, 'rid': rid, 'pos': pos},
      function(data){
        if (data == "OK") {
          status_color = green; // shade of green
        }
        else {
          status_color = red; // shade of red
        }
        //alert("Server Response: " + data + "\n\nQueue: " + queue + "\nOrig Row: "+ row_id + "\nRID is: " + rid + "\nNew Position: " + pos );
        $(row_id).effect("highlight", { color: status_color }, timeout);
        
        // Reload the current tab
        var current_index = $("#tabs").tabs("option","selected");
        setTimeout(function() { $("#tabs").tabs("load", current_index); }, timeout);
      }
    );
  }
  else {
    $(row_id).effect("highlight", { color: red }, timeout);
    
    // Reload the current tab
    var current_index = $("#tabs").tabs("option","selected");
    setTimeout(function() { $("#tabs").tabs("load", current_index); }, timeout);
  }
}
