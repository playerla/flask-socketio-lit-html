import resolve from 'rollup-plugin-node-resolve';
import minify from 'rollup-plugin-minify-es';

export default {
	input: ['dependencies.js'],
	output: {
		file: '../flask_socketio_lit_html/webcomponents_static/element.js',
		format: 'cjs',
		sourcemap: false
	},
	plugins: [
        resolve(),
        minify()
  ]
};
