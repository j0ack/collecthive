<template>
  <section class="books-index">
    <h1 class="title">
      Books
    </h1>
    <div class="pure-g content">
      <div class="pure-u-3-4 books">
        <p
          v-if="books.length === 0"
        >
          No books
        </p>

        <div
          v-else
          class="pure-g grid"
        >
          <Link
            v-for="book in books"
            :key="book.id"
            :title="book.title"
            :href="$route('books.book_detail', book.isbn)"
            class="pure-u-1-6 link"
          >
            <img
              :src="book.cover"
              alt="cover"
              class="pure-img cover"
            >
          </Link>
        </div>
        <div class="pages">
          <button
            class="pure-button page"
            :class="(page === current_page) ? ' button-primary' : ' button-secondary'"
            v-for="page in pages"
            :key="page"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </div>
      </div>
      <div class="pure-u-1-4 pure-menu menu">
        <ul class="pure-menu-list menulist">
          <li class="pure-menu-item menuitem">
            <Link
              :href="$route('books.create_book')"
              class="pure-menu-link link"
            >
              Create a new book
            </Link>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import Layout from '@/common/Layout.vue';
import { router } from '@inertiajs/vue3';
import { Link } from '@inertiajs/vue3';
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

export default defineComponent({
  name: 'BooksIndex',
  layout: Layout,
  components: {
    Link
  },
  props: {
    books: {
      type: Array as PropType<Book[]>,
      required: true
    },
    pages: {
      type: Array as PropType<number[]>,
      required: true
    },
    current_page: {
      type: Number as PropType<number>,
      required: true,
      default: 1
    }
  },
  methods: {
    goToPage(pageNumber: number) {
      const endpoint: string = this.$route("books.index");
      router.get(endpoint, { page: pageNumber });
    }
  }
});
</script>

<style scoped>
.books-index {
  > .content > .menu {
    background-color: rgb(254 215 170);
  }
  > .content > .menu > .menulist > .menuitem > .link {
    color: black;
  }
  > .content > .books > .grid > .link {
    padding: .5rem;
  }
  > .content > .books > .grid > .link > .cover {
    height: 18rem;
  }
  > .content > .books > .pages {
    margin-top: 1rem;
  }
  > .content > .books > .pages > .page {
    margin: 0 .25rem;
  }
}
</style>
