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
	{id:16, abbr: "C", name: "Composition"},
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

function getgerval() {
	var genedreqs = 0;
	$("input[name=ger]:checked").each(function() {
		genedreqs |= genedreqCodeToNumber($(this).val());
	});

 	return genedreqs;
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
    	var genedreqs = getgerval();
     	if(genedreqs > 0) {
     		params['ger'] = genedreqs;
     	}

     	/*
     	 * start time
     	 *
     	 */
     	 var startTime = $('#starttime').val();
     	 if(startTime !== undefined && startTime.length > 0) {
     	 	params['starttime'] = startTime;
     	 }

     	/*
     	 * end time
     	 *
     	 */
     	 var endTime = $('#endtime').val();
     	 if(endTime !== undefined && endTime.length > 0) {
     	 	params['endtime'] = endTime;
     	 }


     	 query.set(params);

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

		if(this.model.get('ger') > 0) {
			var ger = this.model.get('ger');
			$('input[name="ger"]').each(function(d,i){
				console.dir(d);
			});
		};

	}, 

	events: {
		"change input": "changed",
	},

	changed: function(ev) {
		console.log('input changed: ' + $(ev.srcElement).attr('name'));
		console.dir(ev);
		console.dir($(ev.srcElement).val());
		var name = $(ev.srcElement).attr('name');
		if( name === 'ger') {
			var newval = getgerval();
			var oldval = query.get('ger');
			console.log('ger changed: from "' + oldval + '" to "' + newval + '"')
			query.set('ger', getgerval());
		}
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
		var lastpage = (curpage > 2) ? Math.min(maxpages, curpage + 3) : Math.min(maxpages, 5);
		var firstpage = (curpage > 2) ? Math.max(0, lastpage - 5) : 0;



		console.log('maxpages = ' + maxpages );
		console.log('curpage = ' + curpage );
		console.log('firstpage = ' + firstpage );
		console.log('lastpage = ' + lastpage );

		if(maxpages > 0) {
			var html = '<div class="pagination"><ul>'

			html += '<li' + (curpage <= 0 ? ' class="disabled"' : '') + '><a data-page="' + ((curpage -1) >= 0 ? (curpage-1) : '') +'" href="#">Prev</a></li>';
			console.log('prev page is: ' + (curpage-1));
			for(var i = firstpage; i < lastpage; i++ ) {
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
		console.log('offset is now: ' + offset );
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
			model: this.model,
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
	"offset": 0,
		"limit": 20,
		"ger": 0,
		"starttime": null,
		"endtime": null,
		"query": "",
		"offered": false,
		"open": false,
*/

function copyIfNotDefault(q, prop, defaultval) {
	if(query.get(prop) !== defaultval) { q[prop] = query.get(prop); }

	return q;
}

function buildQueryString() {
	var q = {}

	q = copyIfNotDefault(q, 'offset', 0);
	q = copyIfNotDefault(q, 'limit', 20);
	q = copyIfNotDefault(q, 'ger', 0);
	q = copyIfNotDefault(q, 'starttime', null);
	q = copyIfNotDefault(q, 'endtime', null);
	q = copyIfNotDefault(q, 'query', '');
	q = copyIfNotDefault(q, 'offered', false);
	q = copyIfNotDefault(q, 'open', false);	

	return q;
}

function doQuery() {
	q = buildQueryString();

	var spinner = $('#results').first().spin("small" );

	// request our data
	$.ajax( BASE_URL + 'api/v1/course/?' + $.param(q) + '', {
		dataType: 'json',
		success: function(data) {
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
					"name": ((d.name.length > 32) ? (d.name.substring(0,32) + '...'): d.name),
					"credits": d.mincredits,
					"enrollment": enrollment,
					"genedreqs": GenEdCodeToAbbrString(d.genedreqs)
				}
			});

			courselist.reset(rows);
			querymeta.set(data.meta);

			console.log("rows");
			console.dir(rows);
			
		}

	});
}


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
        	el: '#main',
        	model: query,
      	});

	},

	search: function(querystr) {
		console.log('search!');
		console.dir(querystr);

		var params = parseQueryString(querystr);
    	console.dir(params);

		query.set(params);
		this.results = this.results || new ResultsView({
		        	el: '#main',
		        	model: query,
		      	});

		doQuery();
	},


});



/*
 *
 *
 * event handler
 *
 *
 */

queryEvent.on("all", function(eventname){
	console.log("queryEvent all: " + eventname );
	console.dir(query.toJSON());
	app.navigate('search/?' + $.param(buildQueryString()), {trigger: true} );
});

query.on("change", function(){ 
	queryEvent.trigger('change');
});

