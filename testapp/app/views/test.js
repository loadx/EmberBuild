minispade.require('core');

App.TestView = Ember.View.extend({
  templateName: 'outlet',
  didInsertElement: function(){
    this.get('parentView').set('buttonStateDisabled', true);
  }
});
