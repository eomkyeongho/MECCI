const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  },
  
  devServer: {
    port : 8080,
    host : '0.0.0.0',
    proxy : 'http://localhost:8000'
  }
})