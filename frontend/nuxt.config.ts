// frontend/nuxt.config.ts
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  ssr: false,
  output: 'static',
  app: {
    head: {
      title: '手書き文字認識',
      meta: [
        { name: 'description', content: 'ユニラブ2025で使用する手書き文字認識アプリです' },
        { name: 'viewport',   content: 'width=device-width, initial-scale=1' },
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/igem-logo.png' }
      ]
    }
  }
  // nitro, runtimeConfig 等は必要に応じて追加
})
