import resolve from 'rollup-plugin-node-resolve';
import minify from 'rollup-plugin-babel-minify';

export default {
	input: ['dependencies.js'],
	output: {
		file: '../webcomponents_static/element.js',
		format: 'cjs',
		sourcemap: false
	},
	plugins: [
        resolve(),
        minify({comments: false})
  ]
};
