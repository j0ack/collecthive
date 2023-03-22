<template>
  <Layout>
    <PageTitle>Books</PageTitle>
    <section class="w-full">
      <p
        v-if="books.length === 0"
        class="font-bold text-center"
      >
        No books
      </p>

      <div
        v-else
        class="grid grid-cols-10 gap-2"
      >
        <img
          v-for="book in books"
          :key="book.id"
          :title="book.title"
          :src="book.cover"
          alt="cover"
          class="h-52 w-auto m-auto"
        >
      </div>
    </section>
  </Layout>
</template>

<script lang="ts">
import Layout from '@/common/Layout.vue';
import PageTitle from '@/common/PageTitle.vue';
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

export default defineComponent({
  name: 'BooksIndex',
  components: {
    Layout,
    PageTitle,
  },
  props: {
    books: {
      type: Array as PropType<Book[]>,
      required: true
    }
  }
});
</script>
