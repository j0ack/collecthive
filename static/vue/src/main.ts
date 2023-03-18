import { createApp, h } from 'vue';
import type { App, DefineComponent } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import './index.css';

type StrOrNum = string | number

declare global {
  interface Window {
    reverseUrl(
      urlName: string,
      args?: Record<string, unknown> | StrOrNum | StrOrNum[]
    ): string
  }
}

// create a plugin to use window.reverseUrl in our Components
const routePlugin = {
  install: (app: App, _options: Record<string, unknown>) => {
    app.config.globalProperties.$route = window.reverseUrl;
  }
};

createInertiaApp({
  resolve: (name: string) => {
    const pages = import.meta.glob('./pages/**/*.vue');
    return pages[`./pages/${name}.vue`]() as Promise<DefineComponent>;
  },
  setup({ el, App, props, plugin }) {
    const vueApp = createApp({ render: () => h(App, props) });
    vueApp.use(plugin);
    vueApp.use(routePlugin, {});
    vueApp.mount(el);
  }
});
