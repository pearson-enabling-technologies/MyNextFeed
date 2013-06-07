/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true */
/*global MealPlanner, Backbone*/

(function() {
    MealPlanner.DayModel = Backbone.Model.extend({
        initialize : function(dayData) {
            var meals = ['breakfast', 'lunch', 'dinner'];
            meals.forEach(function(key) {
                this.set(key, new MealPlanner.RecipesCollection(dayData[key]));
            }.bind(this));
            this.set('mealNames', ['breakfast', 'lunch', 'dinner']);
        }
    });
}());
