module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:vue/strongly-recommended',
    'plugin:@typescript-eslint/recommended'
  ],
  env: {
    node: true
  },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
  },
  plugins: [
    'vue',
    '@typescript-eslint'
  ],
  root: true,
  rules: {
    'semi': [2, 'always'], // error without semi colons
    'indent': ['error', 2], // error unless indention uses 2 spaces
    'object-curly-spacing': ['error', 'always'], // spaces around curly braces
    'max-len': ['error', { 'code': 89 }], // lines are 89 characters max
    // disable rules for TS and Vue3
    '@typescript-eslint/no-unused-vars': 'off',
    'vue/multi-word-component-names': 'off',
    'vue/no-multiple-template-root': 'off',
    'vue/no-reserved-component-names': 'off',
    'no-undef': 'off',
  }
};
