/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true, nomen: true */
/*global MealPlanner, Backbone, _*/

MealPlanner.DayView = Backbone.View.extend({
    initialize : function(options) {
        var self = this;
        var model = options.model;
        this.subviews = {};
        model.get('mealNames').forEach(function(mealName) {
            self.subviews[mealName] = new MealPlanner.RecipeView({
                model: model.get(mealName).at(0)
            });
        });

    },
    render     : function() {
        this.$el.empty();
        this.model.get('mealNames').forEach(function(mealName) {
            this.subviews[mealName].render();
            this.$el.append(this.subviews[mealName].el);
        }.bind(this));
    },
    className  : 'day'
});
