import { createPinia, defineStore } from 'pinia'

const _delay = (t: number) => new Promise((r) => setTimeout(r, t))

export const useShared = defineStore('shared', {
  state: () => ({
    lat: null,
    lon: null, 
    location: 'Madrid, España',
    locationTyped: 'Madrid, España',
    imageEncoded: null,
    promoCode: null
  }),
  
  actions: {
    async delay(n:number) {
      await _delay(n)
    }
  },
})

const store = createPinia()

export default store