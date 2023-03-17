import { shallowMount } from '@vue/test-utils';
import Index from '@/pages/Index.vue';

describe('Index.vue', () => {
  test('mount', () => {
    const wrapper = shallowMount(Index);
    expect(wrapper).toBeTruthy();
  });
});
