App.Router = Ember.Router.extend({
    enableLogging: true,

    root: Ember.Route.extend({
        doTest: Ember.Route.transitionTo('two'),
        index: Ember.Route.extend({
            route: '/'
        })
    }),

    two: Ember.Route.extend({
        route: '/two',
        connectOutlets: function(router){
            router.get('applicationController').connectOutlet('test');
        }
    })
});