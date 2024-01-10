<template>
  <div class="flex items-center justify-center">
    <div
      class="grid items-center justify-center pt-8 px-4 border-t grid-cols-1 md:grid-cols-2"
    >
      <!-- Two columns: left for the search elements, right for the image -->
      <div
        class="grid grid-flow-row auto-rows-max overflow:hidden justify-center mb-4 mt-4 text-lg"
      >
        <div>
          <h3
            class="flex justify-start mb-4 ml-4 text-lg font-medium text-gray-900 dark:text-white"
          >
            Select your city, region or country
          </h3>
        </div>

        <!-- Dropdown menu -->
        <div
          id="dropdownSearch"
          class="z-10 bg-white rounded-lg shadow w-96 dark:bg-gray-700"
        >
          <div class="p-3">
            <label for="input-group-search" class="sr-only">Search</label>
            <div class="relative">
              <div
                class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
              >
                <svg
                  class="w-4 h-4 text-gray-500 dark:text-gray-400"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 20"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
                  />
                </svg>
              </div>
              <input
                type="text"
                id="input-group-search"
                class="block w-full p-2 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                :placeholder="placeholder || 'Search'"
                v-model="locationTyped"
                @keyup="search"
                :aria-expanded="places.length > 0 ? true : false"
              />
            </div>
          </div>
          <!-- Options from dropdown -->
          <ul
            class="h-48 px-3 pb-3 overflow-y-auto text-sm text-gray-700 dark:text-gray-200"
            v-if="places.length > 0"
          >
            <li
              v-for="place in places"
              :key="place.place_id"
              @click="selectPlace(place)"
            >
              <div
                class="flex items-center pl-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600"
              >
                <label
                  class="w-full py-2 ml-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300"
                >
                  {{ place.description }}</label
                >
              </div>
            </li>
            <a
              href="#"
              class="flex items-center p-3 text-sm font-medium text-red-600 border-t border-gray-200 rounded-b-lg bg-gray-50 dark:border-gray-600 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-red-500 hover:underline"
              @click="closeSuggestions"
            >
              <svg
                fill="#FA5252"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 30 30"
                class="w-4 h-4 mr-2"
                height="30px"
              >
                <path
                  d="M 7 4 C 6.744125 4 6.4879687 4.0974687 6.2929688 4.2929688 L 4.2929688 6.2929688 C 3.9019687 6.6839688 3.9019687 7.3170313 4.2929688 7.7070312 L 11.585938 15 L 4.2929688 22.292969 C 3.9019687 22.683969 3.9019687 23.317031 4.2929688 23.707031 L 6.2929688 25.707031 C 6.6839688 26.098031 7.3170313 26.098031 7.7070312 25.707031 L 15 18.414062 L 22.292969 25.707031 C 22.682969 26.098031 23.317031 26.098031 23.707031 25.707031 L 25.707031 23.707031 C 26.098031 23.316031 26.098031 22.682969 25.707031 22.292969 L 18.414062 15 L 25.707031 7.7070312 C 26.098031 7.3170312 26.098031 6.6829688 25.707031 6.2929688 L 23.707031 4.2929688 C 23.316031 3.9019687 22.682969 3.9019687 22.292969 4.2929688 L 15 11.585938 L 7.7070312 4.2929688 C 7.5115312 4.0974687 7.255875 4 7 4 z"
                />
              </svg>
              Clear
            </a>
          </ul>
        </div>
      </div>

      <div
        class="flex items-center justify-center max-w-lg h-auto px-5 md:px-10 py-4"
        :class="showSpinner ? 'opacity-50' : 'opacity-100'"
      >
        <div
          class="relative items-center block max-w-sm p-6 bg-white border border-gray-100 rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-800 dark:hover:bg-gray-700"
        >
          <img
            v-bind:src="imageEncoded"
            height="200"
            alt="ShowLocalStripes image from location"
          />

          <div
            role="status"
            v-if="showSpinner"
            class="absolute -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2"
          >
            <svg
              aria-hidden="true"
              class="w-10 h-10 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill"
              />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      </div>

      <!-- Modal for too many requests -->
      <div
        v-if="showModal"
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div
          class="flex items-start justify-center min-h-screen pt-32 px-8 pb-20 text-center"
        >
          <!-- Background overlay -->
          <div
            class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
            @click="showModal = false"
          ></div>

          <!-- Modal content -->
          <div
            class="inline-block align-top bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all"
          >
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <h3
                class="text-lg leading-6 font-medium text-gray-900"
                id="modal-title"
              >
                Oops! Too many requests
              </h3>
              <div class="mt-2">
                <p class="text-md text-gray-500">
                  We have reached the maximum number of allowed requests to the
                  open-meteo service for today.
                </p>
                <p class="text-md text-gray-500">
                  Please consider supporting the project by purchasing a t-shirt
                  so we can pay for a higher subscription.
                </p>

                <p class="text-md text-gray-500">Thanks!</p>
                <p class="text-md text-gray-500">
                  Visit some of the existing sites:
                </p>

                <div
                  class="pt-6"
                  v-if="randomStores.length > 0"
                  v-for="({location, lat, lon}, i) in randomStores"
                >
                  <ul
                    class="max-w-md text-gray-500 list-disc list-inside dark:text-gray-400"
                  >
                    <li>
                      <a
                        class="font-small underline text-primary-600 dark:text-primary-500 hover:no-underline"
                        v-bind:href="`https://showyourlocalstripes.com/?location=${location}&lat=${lat}&lon=${lon}`"
                      >
                        {{ location }}</a
                      >
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div
              class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse text-right"
            >
              <button
                type="button"
                @click="showModal = false"
                class="ml-auto w-12 inline-flex justify-right rounded-md border border-transparent shadow-sm px-4 py-2 bg-gray-300 text-3xl font-medium text-white hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mx-3 pr-10 sm:text-2xl"
              >
                🏴‍☠️
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {initFlowbite} from 'flowbite'
import ModalRequests from './modalRequests.vue'

export default {
  props: {
    placeholder: {
      type: String,
      default: 'Enter a location',
    },
    id: {
      type: String,
      default: `places-search-${Math.floor(Math.random() * 100)}`,
    },
  },
  computed: {
    ...mapWritableState(useShared, [
      'lat',
      'lon',
      'location',
      'locationTyped',
      'storeData',
      'imageEncoded',
      'promoCode',
      'showSpinner',
    ]),
  },
  data() {
    return {
      places: [],
      selected: {},
      service: null,
      description: null,
      location_id: null,
      initialized: false,
      showModal: false,
      randomStores: [
        {
          location: 'Pisa, Province of Pisa, Italy',
          lat: 43.7228386,
          lon: 10.4016888,
        },
        {
          location: 'Nuuk, Greenland',
          lat: 64.17432339999999,
          lon: -51.7372787,
        },
        {
          location: 'Madrid, España',
          lat: 40.4167754,
          lon: -3.7037902,
        },
        {
          location: 'Gospić, Croatia',
          lat: 44.5469337,
          lon: 15.3750495,
        },
        {
          location: 'Equador',
          lat: -1.831239,
          lon: -78.18340599999999,
        },
        {
          location: 'Boca de Huérgano, España',
          lat: 42.9726326,
          lon: -4.925356499999999,
        },
        {
          location: 'Vienna, Austria',
          lat: 48.2081743,
          lon: 16.3738189,
        },
        {
          location: 'Dhaka, Bangladesh',
          lat: 23.804093,
          lon: 90.4152376,
        },
        {
          location: 'Jammu, Jammu and Kashmir',
          lat: 32.7266016,
          lon: 74.8570259,
        },
        {
          location: 'Oviedo, España',
          lat: 43.3622522,
          lon: -5.8485461,
        },
      ],
    }
  },
  methods: {
    updateMeta() {
      const metaDescription = document.querySelector(
        'meta[name~="description"]'
      )
      metaDescription.setAttribute('content', this.location)
      const metaOgDescription = document.querySelector(
        'meta[property~="og:description"]'
      )
      metaOgDescription.setAttribute('content', this.location)
      const metaOgImage = document.querySelector('meta[property~="og:image"]')
      metaOgImage.setAttribute('content', this.getThumbnail())
    },
    getThumbnail() {
      if (this.imageEncoded) {
        const config = useRuntimeConfig()
        const url = `${config.public.backend_api_url}/store/image/jpg?store_id=${this.storeData['RNA1']}`
        return url
      } else {
        return 'https://showyourlocalstripes.com/og_image_showyourlocalstripes.png'
      }
    },
    async postStoreData() {
      // POST to backend to get or create the stripes image
      const config = useRuntimeConfig()
      try {
        const requestOptions = {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            location: this.location,
            lat: this.lat,
            lon: this.lon,
            promo_code: this.promoCode,
          }),
        }
        const url = config.public.backend_api_url + '/store/create'
        const response = await fetch(url, requestOptions)
        const data = await response.json()
        const status = response.status
        return {data: data, status: status}
      } catch (error) {
        throw error
      }
    },
    async getStoreImage() {
      // GET to backend, to fetch the iage url
      if (this.storeData) {
        const config = useRuntimeConfig()
        try {
          // Get the stripes image
          // The stripes image is the same or all items, use one type (fx, RNA1)
          const url = `${config.public.backend_api_url}/store/image?store_id=${this.storeData['RNA1']}`
          const response = await fetch(url)
          const data = await response.json()
          const status = response.status
          return {data: data, status: status}
        } catch (error) {
          throw error
        }
      }
    },
    async getStoreImageWait() {
      // Loop to fetch the image from backend
      await this.getStoreImage()
        .then((res) => {
          if (res.data.data && res.status === 200) {
            this.imageEncoded = 'data:image/png;base64,' + res.data.data
            this.showSpinner = false
            this.updateMeta()
          } else {
            setTimeout(this.getStoreImageWait, 100)
          }
        })
        .catch((err) => {
          setTimeout(this.getStoreImage, 2000)
        })
    },
    async processDataApi() {
      // Method fired every time the coordinates change
      // IDeally cancel any getStoreImageWait() executions
      // Post info with location and coordinates data
      const fetchData = await this.postStoreData()

      console.log('processDataApi -> fetchData:', fetchData)
      if (fetchData.status === 429) {
        console.log('???? Status 429 -> Show modal')
        this.showSpinner = false
        this.showModal = true
      } else {
        this.storeData = fetchData.data.data
        // Fetch stripes image when ready
        await this.getStoreImageWait()
      }
    },
    async getRandomStores() {
      // GET to backend, to fetch the iage url
      const config = useRuntimeConfig()
      try {
        // Get the stripes image
        // The stripes image is the same or all items, use one type (fx, RNA1)
        const url = `${config.public.backend_api_url}/store/random`
        const response = await fetch(url)
        if (response.status === 200) {
          this.randomStores = await response.json()
        }
      } catch (error) {
        throw error
      }
    },
    async search() {
      try {
        if (this.locationTyped) {
          const results = await this.service.getPlacePredictions({
            input: this.locationTyped,
            // types: ['(regions)'], // TODO, maybe add this as a dropdown filter
            // componentRestrictions: {
            //     country: 'us'
            // }
          })
          this.places = results.predictions
        }
      } catch (error) {
        console.log('error: ', error)
      }
    },
    mapsInit() {
      this.service = new google.maps.places.AutocompleteService()
    },
    getLatLong(location) {
      try {
        self = this
        const geocoder = new google.maps.Geocoder()
        geocoder.geocode(
          {
            placeId: location,
          },
          async (results, status) => {
            if (status == google.maps.GeocoderStatus.OK) {
              self.$emit('selectedArea', {
                description: results[0].formatted_address,
                location_id: results[0].place_id,
                lat: await results[0].geometry.location.lat(),
                lon: await results[0].geometry.location.lng(),
              })
              const res = await results[0]
              this.description = res.formatted_address
              this.location_id = res.place_id
              this.lat = res.geometry.location.lat()
              this.lon = res.geometry.location.lng()
              this.updateRoute()
            }
          }
        )
      } catch (error) {}
    },
    selectPlace(place) {
      this.getLatLong(place.place_id)
      this.location = place.description
      this.locationTyped = place.description
      this.selected.description = place.description
      this.selected.location_id = place.place_id
      this.places = []
      this.showSpinner = true
    },
    closeSuggestions() {
      this.places = []
    },
    clearForm() {
      console.log('Clearing form')
      this.locationTyped = ''
      this.location = ''
      this.updateRoute()
      this.selected = {}
      this.places = []
      this.$emit('selectedArea', {})
    },
    updateRoute() {
      const router = useRouter()
      let query = {location: this.location, lat: this.lat, lon: this.lon}
      if (this.promoCode) {
        query = {...query, promo: this.promoCode}
      }
      router.push({
        path: '/',
        query: query,
      })
    },
  },
  watch: {
    lat: 'processDataApi',
    locationTyped() {
      if (this.service === null) {
        if (this.initialized !== false) {
          // Small trick to defer the loading of gmaps
          this.mapsInit()
        }
        this.initialized = true
      }
      if (this.location.length === 0) {
        this.clearForm()
      }
    },
    showModal() {
      console.log('showModal!!!!!!', this.showModal)
      if (this.showModal === true) {
        this.getRandomStores()
      }
    },
  },
  mounted() {
    initFlowbite()
    const config = useRuntimeConfig()
    let recaptchaScript = document.createElement('script')
    recaptchaScript.setAttribute(
      'src',
      `https://maps.googleapis.com/maps/api/js?key=${config.public.googleMapsApiKey}&libraries=places&callback=Function.prototype`
    )
    document.head.appendChild(recaptchaScript)
    this.imageEncoded =
      'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA/IAAAJjCAYAAACvLypqAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy81sbWrAAAACXBIWXMAAA7EAAAOxAGVKw4bAAA/YklEQVR4nO3dd5gkV3kv/u8LSAhQJIMAC2OyCDLG5JyFwRhjcpCNTf7Z3Au2sY0NXDBcTDLXNtlGJIMxXLhkAQKRg8gZBBJJRIEQkkAB6fz+qF4029s902l29+x8Ps/Tj9TVVafO1Ez39rfq1HuqtRYAAACgD+fb1R0AAAAAZifIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANCRCyyz8YXu/u9tnvVvfKtrzNX+1S934Mzr3u9al5mr7Vd9/vtzrf/c775k5nWvfMJt5mr76L+99VzrH3PCj2Ze92oH7T9X2zfc6ztzrX+l5863/jz+/j6HblrbDzzlmLnW3/cvPz7X+g/+h0fOvO5m/+3O47n7HTvX+i8/4JZzrf/kV39h5nXn/f1/8runz7X+9S53kd2i7SR5xNPeNfO6z/ub283X9kP+aa7153HjP7nfprWdJCeccPLM617xigdtYk/m+/dosz3mZleced0f/OyMudq+9IH7zLX+n7760zOv++677jtX20f+6IC51j/ikqdsWtsP/Ohz51r/fHc9YtP6Mq95PnePO/ykudpub/ivudb/zpNeP/O6V/jMa+dq+9vXvedc68/jkNOP27S253XucbO/55L5j8u8P+u5bzpy5nVffsO/mKvteb/DXv85s/+bdOz/eNVcbf/u25881/q5+nVmXvXjh9x1U/ty6n+9c+Z1973OFeZq+7Wvmu97471e98yZ1z31ic+Yq+157Xev28+87iP//MVztX3zA+b7t/S+P/tRzbXBiCvyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAA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'
  },
  components: {ModalRequests},
}
</script>
