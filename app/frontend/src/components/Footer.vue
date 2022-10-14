<template>
  <q-footer class="text-white bg-secondary footer">
    <div class="row footer q-px-xs-xs q-px-lg-lg">
      <div :class="cssOverride">
        <nav id="footer-menu">
          <div>
            <h2 style="color: white !important;">{{ $t("footer.over") }}</h2>
          </div>
          <ul>
            <li>
              <router-link :to="{ name: 'sitemap' }">
                <q-icon color="white" name="keyboard_arrow_right" />
                <span>Sitemap</span>
              </router-link>
            </li>
            <li>
              <router-link :to="{ name: 'overdebromonitor' }">
                <q-icon color="white" name="keyboard_arrow_right" />
                <span>Over de BRO Monitor</span>
              </router-link>
            </li>
            <li>
              <router-link :to="{ name: 'cookies_privacy' }">
                <q-icon color="white" name="keyboard_arrow_right" />
                <span>Cookies en privacy</span>
              </router-link>
            </li>
            <li>
              <router-link :to="{ name: 'kwetsbaarheid-melden' }">
                <q-icon color="white" name="keyboard_arrow_right" />
                <span>Kwetsbaarheid melden</span>
              </router-link>
            </li>
            <li>
              <router-link :to="{ name: 'toegankelijkheid' }">
                <q-icon color="white" name="keyboard_arrow_right" />
                <span>Toegankelijkheid</span>
              </router-link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </q-footer>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  props: {
    cssOverride: {
      default:
        "offset-xs-0 col-xs-12 offset-md-2 col-md-8 q-px-xs-none q-px-lg-lg",
      type: String,
    },
  },
  setup() {
    return {};
  },
});
</script>

<style>
.about {
  font-size: 1.60181rem;
  margin-block-end: 0.5rem;
}

.site-title {
  font-size: 2rem;
  font-family: "RO Serif";
  font-style: italic;
  padding-block-end: 1.67rem;
}

.footer {
  margin-block-start: 1.67rem;
  padding-block-end: 1.67rem;
}

#footer-menu {
  padding: 0 12px;
}
#footer-menu > ul {
  list-style-type: none;
  margin-block-start: 0.5rem;
  margin-block-end: 0.5rem;
  padding-left: 0;
  width: 200px;
}

#footer-menu > ul > li {
  padding-bottom: 0.5rem;
}
</style>
