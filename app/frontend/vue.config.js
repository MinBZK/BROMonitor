const path = require("path");
module.exports = {
  pluginOptions: {
    quasar: {
      importStrategy: "manual",
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
};
