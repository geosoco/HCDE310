/*
 *
 * Spinner helper function
 *
 */

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


/*
 *
 * Query string parser
 *
 */
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
GEN_ED_REQ_CODES = [
	{id: 1, abbr: "NW", name: "Natural World"},
	{id: 2, abbr: "VLPA", name: "Visual Literary and Performing Arts"},
	{id: 4, abbr: "IS", name: "Individuals and Socieites"},
	{id: 8, abbr: "W", name: "Writing"},
	{id:16, abbr: "EC", name: "English Composition"},
	{id:32, abbr: "QSR", name: "Quantitative and Symbolic Reasoning"}
]

function genedreqCodeToNumber(ger) {
	for(var i = 0; i < GEN_ED_REQ_CODES.length; i++) {
		if(GEN_ED_REQ_CODES[i].abbr == ger) {
			return GEN_ED_REQ_CODES[i].id;
		}
	}
}

function GenEdCodeToAbbrString(gerVal) {
	var codes = []
	for(var i = 0; i < GEN_ED_REQ_CODES.length; i++) {
		if((gerVal & GEN_ED_REQ_CODES[i].id) != 0) {
			codes.push(GEN_ED_REQ_CODES[i].abbr);
		}
	}

	return codes.join(', ')
}



/*
 *
 * Models
 *
 */

window.Course = Backbone.Model.extend({

});


window.CourseList = Backbone.Collection.extend({
	model: Course
})

window.QueryMeta = Backbone.Model.extend({

});

window.QueryResult = Backbone.Model.extend({

});


window.Query = Backbone.Model.extend({
	defaults: {
		"page": 0,
		"ger": 0,
		"starttime": null,
		"endtime": null,
		"query": "",
		"offered": false,
		"open": false,
	},
	initialize: function() {

	}

});


courselist = new CourseList();
querymeta = new QueryMeta();
query = new Query();



/*
 *
 * Views
 *
 */

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
     	 	params['starttime'] = startTime;
     	 }

     	/*
     	 * end time
     	 *
     	 */
     	 var endTime = $('#end').val();
     	 if(endTime !== undefined && endTime.length > 0) {
     	 	params['endtime'] = endTime;
     	 }     	 

    	app.navigate('search/?' + $.param(params), {trigger: true} );
    	return false;
    },
    doLookahead: function( event ) {
    	//console.log('doLookahead');
    }

});


FilterPanelView = Backbone.View.extend({

	initialize: function() {
		this.render();
	},

	render: function() {

    	var html = Mustache.render($("#tmpl_filterpanel").html(), {} );
		this.$el.html( html );
	}

});


window.ResultListItem = Backbone.View.extend({
	template: "<tr><td>{{course}}</td><td>{{name}}</td><td>{{credits}}</td><td>{{enrollment}}</td><td>{{genedreqs}}</td></tr>",
	initialize: function() {

	},

	render: function() {
		return Mustache.render(this.template, this.model.toJSON() );
	}
});

window.ResultListView = Backbone.View.extend({
	initialize: function() {
		var results = this.collection;
		results.on("reset", this.render, this);
	},

	render: function() {
		var html = Mustache.render($("#tmpl_resultlist").html(), {} );
		this.$el.html( html );

		_.each(this.collection.models, function (course) {
            $('tbody').append(new ResultListItem({model:course}).render());
        }, this);
	}
});

window.ResultsView = Backbone.View.extend({
	initialize: function() {
		this.render();
		this.filterpanel = new FilterPanelView({
			el: '#filterpanel',
			model: query,
		});
		this.resultlist = new ResultListView({
			el: '#slickgrid',
			collection: courselist
		})
	},

	events: {

	},

	render: function() {

    	var html = Mustache.render($("#tmpl_results").html(), {} );
		this.$el.html( html );
		if(this.filterpanel) {
			this.filterpanel.render();
		}
	}

});






/*
 *
 *
 * Router
 *
 *
 */

window.SearchApp = Backbone.Router.extend({
	
	routes: {
		"": 					"main",
		"search/*query": 		"search", 
	},

	initialize: function(options) {
		console.log('router init');
	},

	main: function() {
    	var search = new SearchView({
        	el: '#main'
      	});

	},

	search: function(query) {
		var page = null;
		console.dir(query);

		var params = parseQueryString(query);
    	console.dir(params);

		search = new ResultsView({
		        	el: '#main'
		      	});

		var spinner = $('#slickgrid').first().spin("small" );

		page = page || 0;




		// request our data
		$.ajax( BASE_URL + 'api/v1/course/?format=json&offset=' + (page * 50) + '&limit=50&' + $.param(params) + '', {
			success: function(data) {
				meta = new QueryMeta(data.meta);

				//console.log('ajax success!');
				console.dir(data);
				spinner.spin(false);

				var columns = [
				    { name: "Course", field: "course", id: "course", width: 100 },
				    { name: "Name", field: "name", id: "name", width: 300 },
				    { name: "Credits", field: "credits", id:"credits", width: 50},
				    { name: "Enrollment", field: "enrollment", id:"enrollment", width: 80},
				    { name: "G.E. Reqs.", field: "genedreqs", id:"genedreqs", width: 80}
				];

				var rows = data.objects.map(function(d,i){

					var enrolled = 0;
					var maxenrolled = -1;

					if(d.sections.length > 0) {
						for(var i = 0; i < d.sections.length; i++ ) {
							enrolled = d.sections[i].numenrolled;
							maxenrolled = d.sections[i].maxenrollment;
						}
					}

					var enrollment = '';
					if(maxenrolled > 0) {
						enrollment = enrolled + "/" + maxenrolled;
					}


					return {
						"course": d.curriculum.abbreviation + " " + d.number,
						"name": d.name,
						"credits": d.mincredits,
						"enrollment": enrollment,
						"genedreqs": GenEdCodeToAbbrString(d.genedreqs)
					}
				});

				courselist.reset(rows);

				console.log("rows");
				console.dir(rows);
				
				//$('#main').html(JSON.stringify(data));
				/*
				slickgrid = new Slick.Grid("#slickgrid",
					rows,
					columns,
					{}
					);
				*/
			}

		});

	},


});






