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
      'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA/IAAAJjCAYAAACvLypqAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuMSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/bCgiHAAAACXBIWXMAAA7EAAAOxAGVKw4bAAA+50lEQVR4nO3dd7xsV103/s+CJARIo5cQTER6F5HeQTCAIiBFWhSl/4TnwYIVEASRojz60EQJTRBBeOihI53QOwQSCAQEUkiD9O/vjz2XnDt35pxp59677nm/X6953Tu7rL3OPjNz5rP3Kq2qAgAAAPThIru6AgAAAMDsBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOrLXsgVc/N7/WrNue8s7XGeusq99lYPm2v5B17/SXNu/+os/mGv753/vpTNve/Xj7jRX2d96/CFzbX/kjw6ca/trXeqAuba/+d7fnXnbqz1/9m2T5LDDLjXX9g+++cFzbT+vh378+TNvu9+/nT1X2Q//68fOtf1mv4bn8fz9j55r+1ccePu5tn/aa7401/avfswt59r+a6ecNtf283jVx0+Ya/t5X8OPeea759r+BX92l/nKf8Tfz7X9PG75ew/atLKT5LjjTplr+3k/b+Yx79+om1zlknNt/+nvnTnX9k+8zWEzb/s/PzlrrrKveNC+c23/+6/57Fzbv+c39ptr+4+fO/vfzHn+ns1bdpL86jueNtf2ufYN59p83s/Wecz7OXzM4SfOtX298T/m2v67T33DzNte9TV/MVfZxz/wb+fafl6HnnnMppY/jwvefORc2897bub9Wc//+yfNtf0rj3jhzNvO+/32pv8w39+oo//Xqze1/PZb95952+NvdL+5yj7kyfeZa/szPn/8XNvvd8OrzrX96149+/fK+z/tIXOVffp/vGuu7ec178/6uBd8aOZtX1SntXnrs4078gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I8gAAANARQR4AAAA6IsgDAABARwR5AAAA6IggDwAAAB0R5AEAAKAjgjwAAAB0RJAHAACAjgjyAAAA0BFBHgAAADoiyAMAAEBHBHkAAADoiCAPAAAAHRHkAQAAoCOCPAAAAHREkAcAAICOCPIAAADQEUEeAAAAOiLIAwAAQEcEeQAAAOiIIA8AAAAdEeQBAACgI4I8AAAAdESQBwAAgI4I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'
  },
  components: {ModalRequests},
}
</script>
