<template>
  <h1 class="font-bold text-3xl my-5">
    <slot />
  </h1>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'PageTitle',
});
</script>
