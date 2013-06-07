/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true, nomen:true */
/*global MealPlanner, Backbone, _*/

MealPlanner.MealCriteriaBar = Backbone.View.extend({
    render : function() {
        this.$el.html(MealPlanner.templates.meal_criteria_bar.render({
            minCalories: 500,
            maxCalories: 5000,
            caloriesStep: 50,
            cuisines : this.cuisines,
            ingredients : this.ingredients
        }));
    },
    initialize: function(data) {
        this.cuisines = _.pairs(data.cuisines).map(function(pair) {
            return {
                name : pair[0],
                count: pair[1]
            };
        }).sort(function(a, b) {
                return a.name > b.name ? 1 : -1;
        });
        this.ingredients = _.pairs(data.ingredients).map(function(pair) {
            return {
                name : pair[0],
                count: pair[1]
            };
        }).sort(function(a, b) {
            return a.name > b.name ? 1 : -1;
        });;
    },
    events : {
        "click .submit" : function() {
            this.trigger('submit', this.$el.find('form').serializeArray());
        },
        "submit form" : function(e) {
            e.preventDefault();
        }
    },
    className: 'criteriaBar'
});