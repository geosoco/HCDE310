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



window.Course = Backbone.Model.extend({

});



window.SearchView = Backbone.View.extend({
    initialize: function(){
    	console.log('searchview init');
    	this.render();
    },

    events: {
    	"click #searchbtn" : "doSearch",
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
    	var str = $('#query').val();
    	app.navigate('search/' + str, {trigger: true} );
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
    	var html = Mustache.render($("#tmpl_result").html(), {} );
		this.$el.html( html );

	}

});


window.SearchApp = Backbone.Router.extend({
	
	routes: {
		"": 					"main", 
		"search/:query":        "search",  		// #search/kiwis
		"search/:query/p:page": "search",   	// #search/kiwis/p7
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

	search: function(query, page) {
		search = new ResultsView({
		        	el: $('#main')
		      	});

		var spinner = $('#slickgrid').first().spin("small" );

		page = page || 0;


		var columns = [
		    {
		        name: "Course",
		        field: "course"
		        id: "course",  // In most cases field and id will have the same value.
		        sortable: true
		    },
		    {
		    	name: "name",
		    	field: "name",
		    	id: "name"
		    }
		];


		$.ajax('/scheduler/api/v1/course/?format=json&offset=' + (page * 50) + '&limit=50&description__icontains=' + query + '', {
			success: function(data) {
				console.log('ajax success!');
				console.dir(data);
				spinner.spin(false);
				
				//$('#main').html(JSON.stringify(data));
				slickgrid = new Slick.Grid("#slickgrid",
					data.objects,
					)

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






