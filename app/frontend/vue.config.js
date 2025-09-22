const path = require("path");
const webpack = require("webpack");

module.exports = {
  pluginOptions: {
    quasar: {
      importStrategy: "combined",
      rtlSupport: false,
    },
  },
  transpileDependencies: ["quasar"],
  chainWebpack: (config) => {
    config // Sets the title of the website
      .plugin("html")
      .tap((args) => {
        args[0].title = "BRO Monitor";
        return args;
      });
    config.module // Used to load in md files
      .rule("md")
      .test(/\.md$/)
      .use("raw-loader")
      .loader("raw-loader")
      .end();
    config.module // Used to remove hashes from the images used by static md files, so we can reference them consistently
      .rule("md-images")
      .test(/\.(png|jpg|jpeg|svg)$/)
      .include.add(path.resolve(__dirname, "src/assets/markdown/images"))
      .end()
      .use("url-loader")
      .loader("url-loader")
      .options({
        limit: 4096,
        fallback: {
          loader: "file-loader",
          options: {
            name: "markdown/images/[name].[ext]",
          },
        },
      })
      .end();
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: JSON.stringify(true),
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(true),
      }),
    ],
    resolve: {
      fallback: {
        stream: require.resolve("stream-browserify"),
      },
      alias: {
        'vue-i18n': 'vue-i18n/dist/vue-i18n.runtime.esm-bundler.js'
      }
    },
  },
};
