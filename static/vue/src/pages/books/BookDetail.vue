<template>
  <div class="pure-g book-detail">
    <div class="pure-u-1-3 covercontainer">
      <img
        class="pure-image cover"
        :src="book.cover"
      >
    </div>
    <div class="pure-u-2-3 bookinfo">
      <h1 class="title">
        {{ book.title }}
      </h1>
      <h2
        class="subtitle"
        v-if="book.subtitle"
      >
        {{ book.subtitle }}
      </h2>
      <p
        class="description"
        v-if="book.description"
      >
        {{ book.description }}
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import Layout from '@/common/Layout.vue';
import { router } from '@inertiajs/vue3';
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

export default defineComponent({
  name: 'BookDetail',
  layout: Layout,
  props: {
    book: {
      type: Object as PropType<Book>,
      required: true
    }
  }
});
</script>

<style scoped>
.book-detail {
  > .covercontainer > .cover {
    max-height: 25rem;
  }
}
</style>
