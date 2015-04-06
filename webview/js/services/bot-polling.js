app.service('BotPolling', function(API, $q, $timeout) {
  this.pollers = {};
  this.rates = {};

  // Start polling for a bot, given the rate of the poll. Returns a deferred
  // promise that will only be updated (via notify) at each poll return, and
  // never be resolved/rejected.
  //
  // Attach to the deferred via the update() method exposed.
  this.start = function(bot, rate) {
    var deferred = $q.defer();

    var that = this;
    that.rates[bot.id] = rate;
    that.pollers[bot.id] = $timeout(function fn() {
      API.botState(bot).then(function(data) {
        deferred.notify(data);
        that.pollers[bot.id] = $timeout(fn, rate);
      });
    }, rate);

    // provide the update() method
    return {
      update: function(cb) {
        deferred.promise.then(null, null, cb);
      }
    };
  };

  this.stop = function(bot) {
    var timeoutId = this.pollers[bot.id];
    $timeout.cancel(timeoutId);
    this.pollers[bot.id] = undefined;
  };

  this.isPolling = function(bot) {
    return this.pollers[bot.id] !== undefined;
  };

  this.pollingRate = function(bot) {
    return this.rates[bot.id];
  };
});
