var path = require('path');

module.exports = function(grunt) {
  // Directories and files
  var rootDir = __dirname, dirs = {
    src: rootDir,
    dest: path.join(rootDir, 'static'),
    jsSrc: path.join(rootDir, 'js'),
  }, files = {
    jade: [ // paths are relative for a reason
      'index.jade',
       path.join('partials', 'dashboard.jade'),
       path.join('includes', 'properties', 'bool.jade'),
       path.join('includes', 'properties', 'point.jade'),
       path.join('includes', 'properties', 'float.jade'),
       // list of partials
    ], js: {
      all: [
        path.join(dirs.jsSrc, 'app.js'),
        path.join(dirs.jsSrc, 'routes.js'),
        path.join(dirs.jsSrc, 'controllers/**/*.js'),
        path.join(dirs.jsSrc, 'directives/**/*.js'),
        path.join(dirs.jsSrc, 'services/**/*.js'),
        path.join(dirs.jsSrc, 'filters/**/*.js'),
        path.join(dirs.jsSrc, 'providers/**/*.js'),
        path.join(dirs.jsSrc, 'factories/**/*.js'),
      ], dist: path.join(dirs.dest, 'js', 'main.js')
    }, packageFile: path.join(rootDir, 'package.json'),
  };

  // Grunt config
  var config = {
    pkg: grunt.file.readJSON(files.packageFile)
  };

  // Concat JS files
  config.concat = {
    options: {
      separator: ';'
    }, dist: {
      src: files.js.all,
      dest: files.js.dist
    }
  };

  // Compress concatenated JS files
  config.uglify = {
    options: {
      mangle: false
    }, dist: {
      files: (function() {
        var ret = {};
        ret[files.js.dist] = files.js.dist;
        return ret;
      })()
    }
  };

  // Compile Jade to HTML
  config.jade = {
    compile: {
      files: (function() {
        var data = {};
        for (var i = 0; i < files.jade.length; i++) {
          var fname = files.jade[i],
              newFname = fname.substr(0, fname.lastIndexOf('.')) + '.html';
          data[path.join(dirs.dest, newFname)] = [path.join(dirs.src, fname)];
        }
        return data;
      })()
    }
  };

  // Watch files and re-run tasks
  config.watch = {
    concat: {
      files: files.js.all,
      tasks: ['concat'],
      interrupt: true
    }, uglify: {
      files: files.js.all,
      tasks: ['concat'],
      interrupt: true
    }, jade: {
      files: files.jade,
      tasks: ['jade'],
      interrupt: true
    }
  };

  // Configure grunt
  grunt.config.init(config);

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jade');

  grunt.task.registerTask('js', ['concat', 'uglify']);
  grunt.task.registerTask('default', ['jade', 'js']);
  grunt.task.registerTask('dev', ['default', 'watch']);
};
