<template>
  <span
    class="align-middle"
    :class="(type) ? `material-icons-${type}` : 'material-icons'"
  >
    {{ icon }}
  </span>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

enum IconType {
  outlined = 'outlined',
  round = 'round',
  sharp = 'sharp',
  'two-tone' = 'two-tone'
}

export default defineComponent({
  name: 'Icon',
  props: {
    type: {
      type: String as PropType<IconType>?,
      default: null,
    },
    icon: {
      type: String as PropType<string>,
      required: true
    }
  },
});
</script>
