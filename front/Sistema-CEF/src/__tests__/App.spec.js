import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import App from '../App.vue'
import HomeView from '../views/HomeView.vue'

const slotStub = {
  template: '<div><slot /></div>',
}

describe('App', () => {
  it('mounts renders properly', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', component: HomeView }],
    })

    await router.push('/')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [router],
        stubs: {
          VApp: slotStub,
          VMain: slotStub,
          VContainer: slotStub,
          VRow: slotStub,
          VCol: slotStub,
          VCard: slotStub,
          VCardTitle: slotStub,
          VCardSubtitle: slotStub,
          VCardText: slotStub,
          VBtn: slotStub,
          VForm: slotStub,
          VTextField: true,
        },
      },
    })

    expect(wrapper.text()).toContain('You did it!')
  })
})
