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
function parseQueryString(querystr) {
	var nvpair = {};
		var qs = querystr.replace('?', '');
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
		"offset": 0,
		"limit": 20,
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
 * Events
 *
 */

var queryEvent = _.extend({}, Backbone.Events);


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
	template: "<tr><th>{{course}}</th><td>{{name}}</td><td>{{credits}}</td><td>{{enrollment}}</td><td>{{genedreqs}}</td></tr>",
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



window.ResultPagerView = Backbone.View.extend({
	initialize: function() {
		var results = this.model;
		results.on("change", this.render, this);
	},

	render: function() {
		var page_size = query.get('limit');
		var maxpages = Math.floor(this.model.get('total_count') / page_size);
		var curpage = Math.floor(this.model.get('offset') / page_size);
		var firstpage = Math.max(0, curpage - 2);
		var lastpage = Math.min(maxpages, curpage + 2);

		console.log('maxpages = ' + maxpages );
		console.log('curpage = ' + curpage );
		console.log('firstpage = ' + firstpage );
		console.log('lastpage = ' + lastpage );

		if(maxpages > 0) {
			var html = '<div class="pagination"><ul>'

			html += '<li' + (curpage <= 0 ? ' class="disabled"' : '') + '><a data-page="' + ((curpage -1) >= 0 ? (curpage-1) : '') +'" href="#">Prev</a></li>';
			console.log('prev page is: ' + (curpage-1));
			for(var i = firstpage; i <= lastpage; i++ ) {
				html += '<li' + (curpage == i ? ' class="active"' : '') + '><a data-page="' + i +'" href="#">' + (i+1) + '</a></li>';
			}
			console.log('next page is: ' + (curpage+1));
			html += '<li' + (curpage > maxpages-1 ? ' class="disabled"' : '') + '><a data-page="' + ((curpage +1) <= maxpages ? (curpage+1) : '') +'" href="#">Next</a></li>';
			html += '</ul></div>';

			this.$el.html(html);
		}
		else {
			this.$el.empty();
		}
	}, 

	pageselected: function(el) {
		console.dir(el);

		console.log();
		console.log('pageselected');
		console.log('active: ' + $(el.srcElement).parent('li').hasClass('active'));
		console.log('disabled: ' + $(el.srcElement).parent('li').hasClass('disabled'));

		var parent = $(el.srcElement).parent('li');

		// ignore if this link is disabled;
		if(parent.hasClass('active') || parent.hasClass('disabled')) {
			return false;
		}

		var page = $(el.srcElement).data('page') || 0;
		var offset = page * query.get('limit');
		query.set('offset', offset );

		// disable standard handling
		return false;
	},

	events: {
		'click a': 'pageselected'
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
			el: '#resultlist',
			collection: courselist
		});

		this.pagerview = new ResultPagerView({
			el: '#pager',
			model: querymeta,
		});

		this.filterpanel.render();
	},

	selected: function(ev) {

	},

	events: {
		"click tr": "selected"
	},

	render: function() {

    	var html = Mustache.render($("#tmpl_results").html(), {} );
		this.$el.html( html );
		if(this.filterpanel) {
			this.filterpanel.render();
		}
		if(this.pagerview) {
			this.pagerview.render();
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

	search: function(querystr) {
		var page = null;
		console.dir(querystr);

		var params = parseQueryString(querystr);
    	console.dir(params);

		search = new ResultsView({
		        	el: '#main',
		      	});

		var spinner = $('#results').first().spin("small" );

		page = page || 0;




		// request our data
		$.ajax( BASE_URL + 'api/v1/course/?format=json&offset=' + query.get('offset') + '&limit=' + query.get('limit') + '&' + $.param(params) + '', {
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
				querymeta.set(data.meta);

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






