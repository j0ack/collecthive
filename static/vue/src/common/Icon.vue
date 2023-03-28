<template>
  <div class="icon-component">
    <span
      class="icon"
      :class="(type) ? `material-icons-${type}` : 'material-icons'"
    >
      {{ icon }}
    </span>
    <span
      class="label"
      v-if="label"
    >{{ label }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

type IconType = null | 'outlined' | 'round' | 'sharp' | 'two-tone';

export default defineComponent({
  name: 'Icon',
  props: {
    type: {
      type: String as PropType<IconType>,
      default: null,
    },
    icon: {
      type: String as PropType<string>,
      required: true,
    },
    label: {
      type: String as PropType<string>,
    }
  },
});
</script>

<style scoped>
.icon-component {
  display: inline-block;
  > .icon {
    margin-right: .25rem;
    vertical-align: middle;
  }
  > .label {
    vertical-align: middle;
  }
}
</style>
