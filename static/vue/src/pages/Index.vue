<template>
  <div class="index-content">
    <img
      class="pure-img logo"
      src="https://flask.palletsprojects.com/en/2.0.x/_static/flask-icon.png"
      alt="Flask logo"
    >
    <img
      class="pure-img logo"
      src="https://avatars.githubusercontent.com/u/47703742?s=200&v=4"
      alt="Inertia logo"
    >
    <img
      class="pure-img logo"
      src="https://vuejs.org/images/logo.png"
      alt="Vue logo"
    >
    <h1 class="title">
      Welcome to your Flask-Inertia {{ frameworkName }} app.
    </h1>
    <p>
      For more information please visit the
      <a
        href="https://flask-inertia.readthedocs.io/"
      >documentation</a>
    </p>
  </div>
</template>

<script lang="ts">
import Layout from '@/common/Layout.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Index',
  layout: Layout,
  data() {
    return {
      frameworkName: 'Vue 3'
    };
  }
});
</script>

<style scoped>
@import '../css/colors.css';

.index-content {
  text-align: center;
  color: $black;
  > .logo {
    height: 5rem;
    margin: 0 .25rem;
    display: inline-block;
  }
}
</style>
