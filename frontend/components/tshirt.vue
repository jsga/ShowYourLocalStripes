<template>
  <section class="bg-white dark:bg-gray-900">
    <div id="Shop" class="py-4 px-4 mx-auto max-w-screen-xl lg:px-6">
      <div class="block mx-auto max-w-screen-sm text-center">
        <p>
          <span>
            <h2
              class="inline mb-8 text-4xl font-extrabold text-gray-900 dark:text-white"
            >
              Spread the word.
            </h2>
          </span>
          <span>
            <h2
              class="inline mb-4 text-4xl tracking-tight font-extrabold leading-tight hover:whitespace-nowrap hover:text-transparent bg-clip-text bg-gradient-to-r hover:to-red-600 hover:from-sky-400"
            >
              Wear your colors.
            </h2>
          </span>
          <span>
            <h2
              class="inline mb-8 text-4xl font-extrabold text-gray-900 dark:text-white"
            >
              Organic 🥦
            </h2>
          </span>
        </p>
      </div>
    </div>

    <!-- Here we could add filter buttons -->
    <!-- DYnamic display of items -->
    <div class="flex justify-center">
      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 border-t border-gray-200"
      >
        <div
          v-if="items.length > 0"
          v-for="(
            {itemCode, itemName, imagePath, priceGbp, storeUrl}, i
          ) in items"
        >
          <div
            class="flex object-contain w-80 h-80 bg-cover bg-center p-12"
            :style="{'background-image': 'url(' + imagePath + ')'}"
          >
            <!-- Display main item and background image, the position depends on the item -->
            <img
              v-if="itemCode == 'RNA1' || itemCode == 'RNB46'"
              class="object-cover mt-8 ml-14 w-30 h-16"
              :src="imageEncoded"
              alt="BannerImage"
            />
            <img
              v-else-if="itemCode == 'RNA7'"
              class="object-cover mt-12 ml-16 w-30 h-16"
              :src="imageEncoded"
              alt="BannerImage"
            />
            <img
              v-if="itemCode == 'RNT1'"
              class="object-cover mt-32 ml-14 w-30 h-16"
              :src="imageEncoded"
              alt="BannerImage"
            />
            <img
              v-if="itemCode == 'RNB14'"
              class="object-cover mt-10 ml-16 w-28 h-16"
              :src="imageEncoded"
              alt="BannerImage"
            />

            <!-- Conditionally display the link to the store, the loader and the tooltip -->
            <div class="flex justify-end items-end">
              <!-- While loading store -->
              <div v-show="storeUrl == null">
                <button
                  type="button"
                  :data-tooltip-target="`tooltip-loading-${i}`"
                  data-tooltip-trigger="hover"
                  class="text-black bg-blue-200 hover:bg-blue-200 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center w-32"
                >
                  <svg
                    aria-hidden="true"
                    role="status"
                    class="inline w-4 h-4 mr-3 text-gray-200 animate-spin dark:text-gray-600"
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
                      fill="#1C64F2"
                    />
                  </svg>
                  {{ Math.ceil(gbpToEur * priceGbp) }}€ &#128722;
                </button>

                <div
                  :id="`tooltip-loading-${i}`"
                  role="tooltip"
                  class="absolute z-1 invisible inline-block px-3 py-2 text-sm font-medium text-black bg-gray-200 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
                >
                  Printing - We are fast but not that much! This will take
                  around 20-30 seconds.
                  <div class="tooltip-arrow" data-popper-arrow></div>
                </div>
              </div>

              <!--  Store ready -->
              <div v-show="storeUrl !== null">
                <button
                  type="button"
                  @click="btnClick(storeUrl)"
                  @mouseover="showTooltip(`tooltip-${i}`, 'hover', $event)"
                  class="text-gray-800 bg-blue-200 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 hover:bg-gradient-to-r hover:to-red-200 hover:from-blue-200 w-auto"
                >
                  &#128722;&nbsp;{{ Math.ceil(gbpToEur * priceGbp) }}€
                </button>

                <div
                  :id="`tooltip-${i}`"
                  role="tooltip"
                  class="absolute z-1 invisible inline-block px-3 py-2 text-sm font-medium text-black bg-gray-200 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-800"
                >
                  Visit store for {{ itemName }}
                  <div class="tooltip-arrow" data-popper-arrow></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      maxRetires: 30,
      sleepTime: 5000,
      gbpToEur: 1.15,
      items: [
        {
          color: 'Grey',
          itemCode: 'RNA1',
          itemName: 'mens plain organic t-shirt',
          imagePath: 'rna1_grey.png',
          priceGbp: 20,
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-XeMwzpqq8rfiRE3lQpm861O0',
        },
        {
          color: 'Red',
          itemCode: 'RNA1',
          itemName: 'mens plain organic t-shirt',
          imagePath: 'rna1_red.png',
          priceGbp: 20,
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-XeMwzpqq8rfiRE3lQpm861O0',
        },
        {
          color: 'Mustard',
          itemCode: 'RNA1',
          itemName: 'mens plain organic t-shirt',
          imagePath: 'rna1_mustard.png',
          priceGbp: 20,
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-XeMwzpqq8rfiRE3lQpm861O0',
        },
        {
          color: 'Light Heather',
          itemCode: 'RNA7',
          itemName: 'mens plain pullover hoodie',
          imagePath: 'rna7_light_heather.png',
          priceGbp: 43,
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-ke0zhRxe1l9t38yNv5KX6ZU1',
        },
        {
          color: 'Red',
          itemCode: 'RNA7',
          itemName: 'mens plain pullover hoodie',
          imagePath: 'rna7_red.png',
          priceGbp: 43,
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-ke0zhRxe1l9t38yNv5KX6ZU1',
        },
        {
          color: 'Khaki',
          itemCode: 'RNB14',
          priceGbp: 20,
          itemName: 'womens crew neck t-shirt',
          imagePath: 'rnb14_khaki.png',
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-pVHuzwMsxqxGhyYtUTsrpHXx',
        },
        {
          color: 'Stone Blue',
          itemCode: 'RNB46',
          priceGbp: 20,
          itemName: 'womens plain t-shirt',
          imagePath: 'rnb46_stone_blue.png',
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-uuwihQmfKji9MrIo0UDP6TCg',
        },
        {
          color: 'White',
          itemCode: 'RNB46',
          priceGbp: 20,
          itemName: 'womens plain t-shirt',
          imagePath: 'rnb46_white.png',
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-uuwihQmfKji9MrIo0UDP6TCg',
        },
        {
          color: 'Natural',
          itemCode: 'RNT1',
          itemName: 'tote bag',
          imagePath: 'rnt1_natural.png',
          priceGbp: 15,
          storeUrl:
            'https://showyourlocalstripes.teemill.com/product/api-TbQsnHvzQUw2iwtfEOPV0jly',
        },
      ],
    }
  },
  computed: {
    ...mapState(useShared, ['storeData', 'location', 'imageEncoded']),
  },
  methods: {
    showTooltip: function (targetElId, triggerType, event) {
      // Fix tooltip v-for, see https://stackoverflow.com/questions/75960896/tooltip-not-works-in-a-loop-flowbite-vue3-tailwindcss3
      const targetEl = document.getElementById(targetElId)
      const tooltip = new Tooltip(targetEl, event.target, {triggerType})
    },

    btnClick: function (storeUrl) {
      if (storeUrl) {
        window.open(storeUrl)
      }
    },

    async fetchCurrencyData() {
      const config = useRuntimeConfig()

      const url = config.public.backend_api_url + '/currency'
      const response = await fetch(url)
      const data = await response.json()
      const status = response.status
      if (status) {
        if (status == 200) {
          this.gbpToEur = data.gbp_to_eur
        }
      }
    },

    async fetchItemData(storeId, counter) {
      const config = useRuntimeConfig()
      if (storeId) {
        const url =
          config.public.backend_api_url + '/store/status?store_id=' + storeId
        const response = await fetch(url)
        const data = await response.json()
        const status = response.status
        if (status) {
          if (status != 200 && counter < this.maxRetires) {
            counter += 1
            setTimeout(this.fetchItemData, this.sleepTime, storeId, counter)
          } else if (status == 200) {
            if (this.items && data.item_code) {
              // Iterate over array and save it where it belongs
              for (let v of this.items)
                if (v.itemCode == data.item_code) {
                  v.storeUrl = data.url
                }
            }
            return {data: data, status: status}
          }
        }
      } else {
        setTimeout(this.fetchItemData, this.sleepTime, storeId)
        return {status: 401}
      }
    },

    async getItemInfo() {
      // Clean store urls
      this.items.forEach((x) => (x.storeUrl = null))

      // Iterate over each of the storeIds until we receive back the store info.
      // Then we save it in the right place inside items
      if (this.storeData) {
        for await (let [item_code, storeId] of Object.entries(this.storeData)) {
          await this.fetchItemData(storeId, 0)
        }
      }
    },
  },

  watch: {
    storeData: 'getItemInfo',
  },
  mounted() {
    this.fetchCurrencyData()
  },
}
</script>
