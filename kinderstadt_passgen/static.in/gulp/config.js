var src = 'src';
var dst = '../static';


module.exports = {
    bower: {
        dst: src + '/vendor'
    },

    browsersync: {
        files: dst + '/**',
        logSnippet: false,
        logLevel: 'silent'
    },

    clean: {
        glob: [ dst + '/**/*', src + '/vendor/**/*' ],
        options: {
            force: true
        }
    },

    code: {
        bundles: [{
            entries: 'order.js',
        }],
        srcBase: src,
        dst: dst,
        uglify: {
            ie_proof: true
        }
    },

    copy: [{
        src: 'node_modules/font-awesome/fonts/*',
        dst: dst + '/fonts/'
    }],

    jshint: {
        src: ['gulpfile.js', 'gulp/**/*.js', src + '/**/*.js', '!' + src + '/vendor/**/*.js']
    },

    styles: {
        src: [
            src + '/home.less',
            src + '/order.less'
        ],
        srcBase: src,
        dst: dst,
        watch: src + '/**/*.less',
        less: {
            paths: ['node_modules']
        },
        minify: {
            keepSpecialComments: 0
        }
    }
};
