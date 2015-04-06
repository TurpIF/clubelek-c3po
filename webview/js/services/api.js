app.service('API', function($http, $q) {
  this.baseUrl = '/api';

  this.getBots = function() {
    var deferred = $q.defer();

    $http.get(this.baseUrl + '/bots').then(function(response) {
      deferred.resolve(response.data.bots);
    });

    return deferred.promise;
  };

  this.botState = function(bot) {
    var deferred = $q.defer(), state = {};

    this.listProperties(bot).then(function(properties) {
      state.properties = properties;
      if (state.simulators) {
        deferred.resolve(state);
      }
    });

    this.listSimulators(bot).then(function(simulators) {
      state.simulators = simulators;
      if (state.properties) {
        deferred.resolve(state);
      }
    });

    return deferred.promise;
  };

  this.listProperties = function(bot) {
    var deferred = $q.defer();

    $http.get(this.baseUrl + '/' + bot.id + '/properties').then(function(response) {
      deferred.resolve(response.data.properties);
    });

    return deferred.promise;
  };

  this.listSimulators = function(bot) {
    var deferred = $q.defer();

    $http.get(this.baseUrl + '/' + bot.id + '/simulators').then(function(response) {
      deferred.resolve(response.data.simulators);
    });

    return deferred.promise;
  };

  this.startSimulator = function(bot, simulatorName) {
    var deferred = $q.defer();

    $http.post(this.baseUrl + '/' + bot.id + '/simulators/' + simulatorName).then(function(response) {
      deferred.resolve(response.data.simulator);
    });

    return deferred.promise;
  };

  this.stopSimulator = function(bot, simulatorName) {
    var deferred = $q.defer();

    $http.delete(this.baseUrl + '/' + bot.id + '/simulators/' + simulatorName).then(function(response) {
      deferred.resolve(response.data.simulator);
    });

    return deferred.promise;
  };
});
