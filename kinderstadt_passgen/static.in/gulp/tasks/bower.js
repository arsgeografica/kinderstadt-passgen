var bower = require('gulp-bower'),
    config = require('../config').bower,
    gulp = require('gulp');


gulp.task('bower', ['clean'], function() {
    return bower(config.dst);
});
