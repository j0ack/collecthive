<template>
  <div class="create-book">
    <section class="pure-g card">
      <form
        class="pure-u-3-4 pure-form pure-form-stacked"
        @submit.prevent="getBookMetadata"
      >
        <label for="from-isbn">ISBN or EAN</label>
        <input
          id="from-isbn"
          v-model="fromIsbn"
          :disabled="withoutIsbn"
          @keyup.enter="getBookMetadata"
          required
        >
        <label
          class="pure-checkbox"
          for="without-isbn"
        >
          <input
            type="checkbox"
            id="without-isbn"
            v-model="withoutIsbn"
          >
          Without ISBN
        </label>
        <button
          type="submit"
          class="pure-button button-secondary"
        >
          Next step
        </button>
      </form>
      <div class="pure-u-1-4 errors" />
    </section>
    <section
      v-if="withoutIsbn || book"
      class="card"
    >
      <BookForm
        :book="book"
        :errors="errors"
        @submit="submit"
      />
    </section>
  </div>
</template>

<script lang="ts">
import BookForm from '@/pages/books/BookForm.vue';
import Layout from '@/common/Layout.vue';
import { router } from '@inertiajs/vue3';
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import type { InertiaBookForm } from '@/pages/books/BookForm.vue';

export default defineComponent({
  name: 'CreateBook',
  components: {
    BookForm
  },
  layout: Layout,
  props: {
    book: {
      type: Object as PropType<Book | null>,
      default: null
    },
    errors: {
      type: Array as PropType<string[]>,
      default: [] as string[],
    },
  },
  data() {
    return {
      fromIsbn: (this.book) ? this.book.isbn : '',
      withoutIsbn: false,
    };
  },
  methods: {
    submit(form: typeof BookForm) {
      const endpoint: string = this.$route('books.create_book');
      form.post(endpoint, {
        forceFormData: true
      });
    },
    getBookMetadata() {
      const endpoint: string = this.$route('books.create_book');
      router.get(endpoint, { isbn: this.fromIsbn });
    }
  }
});
</script>

<style scoped>
@import '../../css/colors.css';

.create-book {
  > .card {
    border: 1px solid $gray;
    padding: .25rem 1rem;
    margin-bottom: 2rem;
  }
}
</style>
