<template>
  <div class="container mx-auto w-3/4 text-center font-mono">
    <img class="max-h-20 mx-2 inline-block" src="https://flask.palletsprojects.com/en/2.0.x/_static/flask-icon.png" alt="Flask logo">
    <img class="max-h-20 mx-2 inline-block" src="https://avatars.githubusercontent.com/u/47703742?s=200&v=4" alt="Inertia logo">
    <img class="max-h-20 mx-2 inline-block" src="https://vuejs.org/images/logo.png" alt="Vue logo">
    <h1 class="font-bold text-3xl my-5">Welcome to your Flask-Inertia {{ frameworkName }} app.</h1>
    <p class="text-slate-500">
      For more information please visit the
      <a class="text-emerald-400" href="https://flask-inertia.readthedocs.io/">documentation</a>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Index',
  data() {
    return {
      frameworkName: 'Vue'
    }
  }
});
</script>
