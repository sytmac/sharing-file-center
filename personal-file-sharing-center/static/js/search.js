$(document).ready(function($){
  $.fn.typeahead.Constructor.prototype.blur = function() {
    var that = this;
    setTimeout(function () { that.hide() }, 250);
	};
	$('#search-dish').typeahead({
		source:function(query,process){
			var tbody = document.getElementById('dir_table')
			var list = new Array()
			for (var i=0;i< tbody.rows.length;i++)
			  {list[i] = tbody.rows[i].cells[0].innerText}
			process(list)
		  }
		})
	})