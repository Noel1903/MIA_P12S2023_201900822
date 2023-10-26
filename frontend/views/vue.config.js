/*const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})*/
const path = require('path');

module.exports = {
  transpileDependencies: true,

  // Configuración específica para el entorno de producción
  productionSourceMap: false, // Desactiva los mapas de origen en producción
  publicPath: '/', // Configura la URL base en producción

  // Configuración personalizada para la compilación de producción
  configureWebpack: {
    optimization: {
      minimize: true, // Minimiza y ofusca el código JS
    },
  },

  // Configuración para manejo de rutas de caché con Service Workers (opcional)
  pwa: {
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      swSrc: 'src/service-worker.js',
    },
  },

  // Configuración para compresión de imágenes (puedes instalar el plugin necesario)
  // Verifica la documentación del plugin correspondiente para detalles
  chainWebpack: (config) => {
    config.module
      .rule('images')
      .use('image-webpack-loader')
      .loader('image-webpack-loader')
      .options({
        mozjpeg: {
          progressive: true,
          quality: 65,
        },
        optipng: {
          enabled: false,
        },
        pngquant: {
          quality: [0.65, 0.90],
          speed: 4,
        },
        gifsicle: {
          interlaced: false,
        },
      });
  },
};

