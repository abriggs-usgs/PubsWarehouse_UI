define([
    'backbone',
    'models/LookupModel',
    'module'
], function(Backbone, LookupModel, module){
        var collection = Backbone.Collection.extend({
        model : LookupModel,
        url : module.config().lookupUrl + 'linkfiletypes?mimetype=json'
    });

    return collection;
});