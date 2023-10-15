export default defineNuxtConfig({
  runtimeConfig: {
    // Public keys that are exposed to the client
    public: {
      googleMapsApiKey:
        process.env.GOOGLE_MAPS_API_KEY || 'DEFAULT_GOOGLE_MAPS_API_KEY',
      backend_api_url: process.env.BACKEND_API_URL || 'http://localhost:5001',
      posthogPublicKey: process.env.POSTHOG_KEY || 'phc_xxxxxxx',
    },
  },
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss'],
  imports: {
    dirs: ['./stores'],
  },
  pinia: {
    autoImports: ['mapWritableState', 'mapState', '@/stores/share'],
  },
})
