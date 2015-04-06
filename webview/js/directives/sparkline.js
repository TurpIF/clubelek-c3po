Highcharts.SparkLine = function (options, callback) {
  var defaultOptions = {
    chart: {
      renderTo: (options.chart && options.chart.renderTo) || this,
      animation: Highcharts.svg,
      backgroundColor: null,
      borderWidth: 0,
      type: 'area',
      margin: [2, 0, 2, 0],
      width: 120,
      height: 20,
      style: {
        overflow: 'visible'
      },
      skipClone: true
    },
    title: {
      text: ''
    },
    credits: {
      enabled: false
    },
    xAxis: {
      labels: {
        enabled: false
      },
      title: {
        text: null
      },
      startOnTick: false,
      endOnTick: false,
      tickPositions: []
    },
    yAxis: {
      endOnTick: false,
      startOnTick: false,
      labels: {
        enabled: false
      },
      title: {
        text: null
      },
      tickPositions: [0]
    },
    legend: {
      enabled: false
    },
    tooltip: {
      useHTML: true,
      hideDelay: 0,
      shared: true,
      positioner: function (w, h, point) {
        return { x: point.plotX - w / 2, y: point.plotY - h};
      },
      headerFormat: '',
      pointFormat: '<b>{point.y}</b>'
    },
    plotOptions: {
      series: {
        animation: true,
        lineWidth: 1,
        shadow: false,
        states: {
          hover: {
            lineWidth: 1
          }
        },
        marker: {
          radius: 0,
          states: {
            hover: {
              radius: 2
            }
          }
        },
        fillOpacity: 0.25
      },
    }
  };

  options = Highcharts.merge(defaultOptions, options);
  return new Highcharts.Chart(options, callback);
};

app.directive('sparkline', function() {
  return {
    restrict: 'E',
    scope: {
      data: '=',
      options: '=',
    },
    link: function(scope, element, attrs) {
      var build = function() {
        var width = $(element[0].parentNode).width();
        var height = $(element[0].parentNode).height();

        $(element[0]).highcharts('SparkLine', {
          chart: {
            width: width,
            height: height,
          },
          series: [{
            data: scope.data,
            pointStart: 1,
          }],
        });
      };

      scope.$watch('data', function(data) {
        if ($(element[0]).highcharts()) {
          $(element[0]).highcharts().series[0].setData(data);
        }
      }, true);

      scope.$watch('options', function(options) {
        build();
      });
    },
    controller: function($scope) {
    },
  };
});

app.directive('sparklineEvolution', function($interval) {
  return {
    restrict: 'E',
    scope: {
      value: '=',
      framerate: '=',
      playing: '=',
      nbData: '@',
      options: '=',
    },
    link: function(scope, element, attrs) {
      scope.nbData = parseInt(scope.nbData);
      var timer = null;

      var build = function() {
        var width = $(element[0].parentNode).width();
        var height = $(element[0].parentNode).height();

        $(element[0]).highcharts('SparkLine', {
          chart: {
            width: width,
            height: height,
          },
          series: [{
            data: scope.data,
            pointStart: 1,
          }],
        });
      };

      var update = function() {
        if ($(element[0]).highcharts()) {
          var serie = $(element[0]).highcharts().series[0];
          serie.addPoint(parseFloat(scope.value),
            true, serie.data.length >= parseInt(scope.nbData));
        }
      };

      scope.$watch('playing', function(playing) {
        if (!playing && timer) {
          $interval.cancel(timer);
          timer = null;
        }
        else if (playing) {
          timer = $interval(update, parseInt(scope.framerate));
        }
      });

      scope.$watch('framerate', function(framerate) {
        if (timer !== null) {
          $interval.cancel(timer);
          timer = $interval(update, parseInt(framerate));
        }
      });

      scope.$watch('options', function(options) {
        build();
      });
    },
    controller: function($scope) {
    },
  };
});
