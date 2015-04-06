app.factory('Bots', function() {
  var bots = [];

  return {
    add: function(name, address) {
      bots.push({
        id: name,
        address: address,
        properties: [],
      });
    }, get: function(name) {
      return bots[name];
    }, all: function() {
      return bots;
    }
  };
});
