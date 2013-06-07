/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true */
/*global MealPlanner, Backbone, $*/

(function() {
    MealPlanner.RecipeView = Backbone.View.extend({
        render : function() {
            var data = this.model.toJSON();
            data.calories = Math.floor(data.calories);
            this.$el.html(MealPlanner.templates.recipe.render(data));
        },
        className: 'course',
        events : {
            "click" : function() {
                var fullDesc = this.$el.find('full-desc');
                console.log(fullDesc);
            }
        }
    });
}());