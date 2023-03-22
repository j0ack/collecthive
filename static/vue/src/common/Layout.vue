<template>
  <header class="w-full mb-5">
    <nav class="py-5 bg-zinc-900">
      <Link
        class="text-orange-400 mx-2 hover:text-orange-500"
        v-for="link in links"
        :key="link.label"
        :href="link.endpoint"
      >
        <Icon
          type="outlined"
          :icon="link.icon"
        />
        <span class="align-middle pl-1">{{ link.label }}</span>
      </Link>
    </nav>
  </header>
  <div class="container mx-auto w-3/4 font-mono">
    <slot />
  </div>
</template>

<script lang="ts">
import Icon from '@/common/Icon.vue';
import { Link } from '@inertiajs/vue3';
import { defineComponent } from 'vue';

interface PageLink {
  endpoint: string;
  label: string;
  icon: string;
}

export default defineComponent({
  name: 'Layout',
  components: {
    Icon,
    Link
  },
  data() {
    return {
      links: [
        {
          endpoint: this.$route('index'),
          label: 'Home',
          icon: 'house',
        },
        {
          endpoint: this.$route('books.index'),
          label: 'Books',
          icon: 'menu_book',
        }
      ] as PageLink[]
    };
  }
});
</script>
