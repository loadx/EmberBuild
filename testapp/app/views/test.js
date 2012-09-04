require('core');

App.TestView = Ember.View.extend({
  templateName: 'templates/outlet',
  didInsertElement: function(){
    this.get('parentView').set('buttonStateDisabled', true);
  }
});
