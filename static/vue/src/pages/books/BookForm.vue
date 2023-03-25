<template>
  <section>
    <form
      @submit.prevent="submit"
      class="pure-form pure-form-stacked"
    >
      <div class="pure-g">
        <div class="pure-u-1-6">
          <img
            v-if="form.cover"
            class="pure-image"
            :src="form.cover"
          >
          <label for="cover">Cover</label>
          <input
            id="cover"
            type="file"
            @input="readFile"
          >
        </div>
        <div class="pure-u-5-6">
          <label for="title">Title</label>
          <input
            class="pure-input-1"
            id="title"
            v-model="form.title"
            placeholder="Title"
            required
          >
          <label for="subtitle">Subtitle</label>
          <input
            class="pure-input-1"
            id="subtitle"
            v-model="form.subtitle"
            placeholder="Subtitle"
          >
          <label for="isbn">ISBN</label>
          <input
            class="pure-input-1"
            id="isbn"
            v-model="form.isbn"
            placeholder="ISBN"
            required
          >
          <label for="authors">Authors</label>
          <input
            class="pure-input-1"
            id="authors"
            v-model="authorList"
            placeholder="Authors"
            data-role="taginput"
          >
          <label for="description">Description</label>
          <textarea
            class="pure-input-1"
            id="description"
            v-model="form.description"
            placeholder="Description"
          />
          <label for="edition">Edition</label>
          <input
            class="pure-input-1"
            id="edition"
            v-model="form.edition"
            placeholder="Edition"
          >
          <label for="status">Status</label>
          <select
            class="pure-input-1"
            id="status"
            v-model="form.status"
          >
            <option
              v-for="(status, index) in statuses"
              :key="index"
              :value="status.value"
            >
              {{ status.label }}
            </option>
          </select>
        </div>
        <button
          class="pure-button button-primary"
          type="submit"
        >
          Submit
        </button>
      </div>
    </form>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useForm } from '@inertiajs/vue3';
import { BOOK_STATUSES } from '@/types/common/types.d';
import type { PropType } from 'vue';
import type { InertiaForm } from '@inertiajs/vue3';
import type { BookStatus } from '@/types/common/types.d';

export type InertiaBookForm = InertiaForm<{
  title: string;
  subtitle: string;
  isbn: string;
  authors: Array<string>;
  description: string;
  edition: string;
  cover: string;
  status: BookStatus;
  coverFile: File | null;
}>;

export default defineComponent({
  name: 'BookForm',
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
  emits: ['submit'],
  data() {
    let coverFile = null;
    let bookForm: Book;
    if (this.book !== null) {
      bookForm = this.book;
    } else {
      bookForm = {
        title: '',
        subtitle: '',
        isbn: '',
        authors: [],
        description: '',
        edition: '',
        cover: '',
        status: 'in_stock'
      } as Book;
    }
    return {
      form: useForm({
        ...bookForm,
        coverFile: coverFile as File | null
      }) as InertiaBookForm,
    };
  },
  computed: {
    authorList: {
      get(): string {
        return this.form.authors.join(',');
      },
      set(newValue: string) {
        this.form.authors = newValue.split(',');
      }
    },
    statuses() {
      return (BOOK_STATUSES).map((status) => {
        return {
          label: status[0].toUpperCase() + status.substring(1).replace(/_/g, ' '),
          value: status
        };
      });
    }
  },
  methods: {
    submit() {
      this.$emit('submit', this.form);
    },
    readFile($event: Event) {
      const element = $event.target as HTMLInputElement;
      const fileList: FileList | null = element.files;
      if (fileList && fileList.length > 0) {
        this.form.coverFile = fileList.item(0);
      }
    }
  }
});
</script>
