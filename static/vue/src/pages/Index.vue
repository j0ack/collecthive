<template>
  <Layout>
    <div class="text-center">
      <img
        class="max-h-20 mx-2 inline-block"
        src="https://flask.palletsprojects.com/en/2.0.x/_static/flask-icon.png"
        alt="Flask logo"
      >
      <img
        class="max-h-20 mx-2 inline-block"
        src="https://avatars.githubusercontent.com/u/47703742?s=200&v=4"
        alt="Inertia logo"
      >
      <img
        class="max-h-20 mx-2 inline-block"
        src="https://vuejs.org/images/logo.png"
        alt="Vue logo"
      >
      <PageTitle>Welcome to your Flask-Inertia {{ frameworkName }} app.</PageTitle>
      <p class="text-slate-500">
        For more information please visit the
        <a
          class="text-emerald-400"
          href="https://flask-inertia.readthedocs.io/"
        >documentation</a>
      </p>
    </div>
  </Layout>
</template>

<script lang="ts">
import Layout from '@/common/Layout.vue';
import PageTitle from '@/common/PageTitle.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Index',
  components: {
    Layout,
    PageTitle
  },
  data() {
    return {
      frameworkName: 'Vue 3'
    };
  }
});
</script>
