module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/base",
    "eslint:recommended",
    "@vue/typescript/recommended",
    "@vue/prettier",
  ],
  plugins: ["@typescript-eslint/eslint-plugin"],
  parserOptions: {
    ecmaVersion: 2022,
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "error" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
    "@typescript-eslint/no-var-requires": 0,
  },
};
