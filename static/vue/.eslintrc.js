module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:vue/essential',
    'plugin:@typescript-eslint/recommended'
  ],
  env: {
    node: true
  },
  parser: '@typescript-eslint/parser',
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
    '@typescript-eslint/no-unused-vars': 'off',
  }
};
