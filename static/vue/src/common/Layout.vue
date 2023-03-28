<template>
  <header class="pure-menu pure-menu-horizontal layout-header">
    <nav class="pure-menu-list nav">
      <Link
        class="pure-menu-item pure-menu-link link"
        v-for="link in links"
        :key="link.label"
        :href="link.endpoint"
      >
        <Icon
          type="outlined"
          :icon="link.icon"
          :label="link.label"
        />
      </Link>
    </nav>
  </header>
  <div class="layout-content">
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

<style scoped>
@import '../css/colors.css';

.layout-header {
  margin-bottom: 2rem;
  background-color: $black;
  > .nav {
    padding: 1rem 0;
  }
  > .nav > .link {
    color: $primary;
  }
  > .nav > .link:focus,
  > .nav > .link:hover {
    color: $primary-light;
    background-color: $black;
  }
}
.layout-content {
  width: 80%;
  margin: auto;
}
</style>
