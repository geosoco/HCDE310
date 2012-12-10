$.fn.spin = function(opts) {
  this.each(function() {
    var $this = $(this),
        data = $this.data();

    if (data.spinner) {
      data.spinner.stop();
      delete data.spinner;
    }
    if (opts !== false) {
      data.spinner = new Spinner($.extend({color: $this.css('color')}, opts)).spin(this);
    }
  });
  return this;
};

function parseQueryString(query) {
	var nvpair = {};
		var qs = query.replace('?', '');
    	var pairs = qs.split('&');
    	$.each(pairs, function(i, v){
      		var pair = v.split('=');
      		nvpair[pair[0]] = pair[1];
    	});

    return nvpair;
}

/*
    NW = 1
    VLPA = 2
    IS = 4
    W = 8
    EC = 16
    QSR = 32
*/
function genedreqCodeToNumber(ger) {
	switch(ger) {
		case 'NW': return 1;
		case 'VLPA': return 2;
		case 'IS': return 4;
		case 'W': return 8;
		case 'EC': return 16;
		case 'QSR': return 32;
		default: return 0;
	}
}


window.Course = Backbone.Model.extend({

});



window.SearchView = Backbone.View.extend({
    initialize: function(){
    	console.log('searchview init');
    	this.render();
    },

    events: {
    	"click #searchbtn" : "doSearch",
    	"submit form" : "doSearch",
    	"keypress #query" : "doLookahead",
    },
    render: function() {
    	// render with our template
    	//var tmpl = _.template( $("#tmp_search").html(), {} );
    	var html = Mustache.render($("#tmpl_search").html(), {} );
		this.$el.html( html );
    },

    doSearch: function( event ) {
    	console.log('doSearch');
    	var params = {};

    	/*
    	 * query string
    	 *
    	 */
    	var str = $('#query').val().trim();
    	if(str !== undefined && str.length > 0) {
    		params['query'] = str;
    	}

    	/*
    	 *
    	 * genedreqs
    	 */
    	var genedreqs = 0;
     	$('input[name="ger"] :checked').each(function() {
       		genedreqs |= genedreqCodeToNumber($(this).val());
     	});
     	if(genedreqs > 0) {
     		params['ger'] = genedreqs;
     	}

     	/*
     	 * start time
     	 *
     	 */
     	 var startTime = $('#start').val();
     	 if(startTime !== undefined && startTime.length > 0) {
     	 	params['sections__meetings__starttime__gte'] = startTime;
     	 }

     	/*
     	 * end time
     	 *
     	 */
     	 var endTime = $('#end').val();
     	 if(endTime !== undefined && endTime.length > 0) {
     	 	params['sections__meetings__endtime__lte'] = endTime;
     	 }     	 

    	app.navigate('search/?' + $.param(params), {trigger: true} );
    	return false;
    },
    doLookahead: function( event ) {
    	console.log('doLookahead');
    }

});


window.ResultsView = Backbone.View.extend({
	initialize: function() {
		this.render();
	},

	events: {

	},

	render: function() {

    	var html = Mustache.render($("#tmpl_results").html(), {} );
		this.$el.html( html );
		console.log('results done')
	}

});


window.SearchApp = Backbone.Router.extend({
	
	routes: {
		"": 					"main",
		"search/*query": 		"search", 
		"curriculums":			"browseCurriculums",
		"courses":				"browseCourses",
		"instructors":			"browseInstructors",
	},

	initialize: function(options) {
		console.log('router init');
	},

	main: function() {
    	var search = new SearchView({
        	el: $('#main')
      	});

	},

	search: function(query) {
		var page = null;
		console.dir(query);

		var params = parseQueryString(query);
    	console.dir(params);

		search = new ResultsView({
		        	el: $('#main')
		      	});

		var spinner = $('#slickgrid').first().spin("small" );

		page = page || 0;




		$.ajax( BASE_URL + 'api/v1/course/?format=json&offset=' + (page * 50) + '&limit=50&' + $.param(params) + '', {
			success: function(data) {
				console.log('ajax success!');
				console.dir(data);
				spinner.spin(false);

				var columns = [
				    { name: "Course", field: "course", id: "course", sortable: true, width: 100 },
				    { name: "Name", field: "name", id: "name", width: 300 },

				];

				var rows = data.objects.map(function(d,i){
					return {
						"course": d.curriculum.abbreviation + " " + d.number,
						"name": d.name
					}
				});

				console.log("rows");
				console.dir(rows);
				
				//$('#main').html(JSON.stringify(data));
				slickgrid = new Slick.Grid("#slickgrid",
					rows,
					columns,
					{}
					);

			}

		});

	},

	browseCurriculums: function() {

	},

	browseCourses: function() {

	},

	browseInstructors: function() {

	}

});






