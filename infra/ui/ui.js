"use strict";

// RPC wrapper
function invoke_rpc(method, args, timeout, on_done){
  $("#crash").hide();
  $("#timeout").hide();
  $("#rpc_spinner").show();
  //send RPC with whatever data is appropriate. Display an error message on crash or timeout
  var xhr = new XMLHttpRequest();
  xhr.open("POST", method, true);
  xhr.setRequestHeader('Content-Type','application/json; charset=UTF-8');
  xhr.timeout = timeout;
  xhr.send(JSON.stringify(args));
  xhr.ontimeout = function () {
    $("#timeout").show();
    $("#rpc_spinner").hide();
    $("#crash").hide();
  };
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      $("#rpc_spinner").hide();
      var result = JSON.parse(xhr.responseText)
      $("#timeout").hide();
      if (typeof(on_done) != "undefined"){
        on_done(result);
      }
    } else {
      $("#crash").show();
    }
  }
}

// Resource load wrapper
function load_resource(name, on_done) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", name, true);
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      on_done(result);
    }
  }
  xhr.send();
}

// Code that runs first
$(document).ready(function(){
  restart();
  init();
});

function restart(){
  invoke_rpc( "/restart", {} )
}

//  LAB CODE

[[ ui ]]
