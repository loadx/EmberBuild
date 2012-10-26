var get = Ember.get;
var template_path = 'templates'

Ember.View.reopen({
  templateForName: function(name, type) {
    if (!name) { return; }

    var templates = get(this, 'templates'),
        template = get(templates, name);

    if (!template) {
      template = minispade.require(template_path + '/' + name);
      if (!template) {
        template = this._super(name, type);
      }
    }

    return template;
  }
});
