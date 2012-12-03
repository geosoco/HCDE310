

var Router = Backbone.Router.extend({
	
	routes: {
		"help":                 "help",    		// #help
		"search/:query":        "search",  		// #search/kiwis
		"search/:query/p:page": "search",   	// #search/kiwis/p7
		"curriculums":			"browseCurriculums",
		"courses":				"browseCourses",
		"instructors":			"browseInstructors",
	},

	help: function() {

	},

	search: function(query, page) {
    
	},

	browseCurriculums: function() {

	},

	browseCourses: function() {

	},

	browseInstructors: function() {
	
	}

})