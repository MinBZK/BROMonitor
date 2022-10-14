<template>
    <q-breadcrumbs >
      <span class="assistive" id="breadCrumbNavLabel">U bevindt zich hier:</span>
        <template v-slot:separator>
            <q-icon
                name="keyboard_arrow_right"
                size="1.5rem"
            />
        </template>
        <q-breadcrumbs-el class="header-text" label="BRO Monitor" to="/"/>
        <q-breadcrumbs-el v-for="crumb in crumbs" :key="crumb.path" v-bind:label="crumb.text" v-bind:to="crumb.to"/>
    </q-breadcrumbs>
</template>

<script>
export default {
  methods: {
      sanitizePath(path){
          const pathCapitalized = path.charAt(0).toUpperCase() + path.slice(1);
          let pathSanitized = pathCapitalized.replace(/-/g, " ");
          if (pathSanitized == 'Over de bro monitor') {
            pathSanitized = 'Over de BRO Monitor';
          }
          return pathSanitized;
      }
  },
  computed: {
    crumbs: function() {
      const pathArray = this.$route.fullPath.split("/")
      pathArray.shift()
      const breadcrumbs = []
      let fullPath = ""
      let crumbText = ""
      pathArray.forEach(p => {
        fullPath += "/" + p;
        if (p.toLowerCase() !== ""){
          crumbText = this.$i18n.t(this.$router.resolve({path: fullPath}).route.meta?.breadCrumb) || this.sanitizePath(p)
          if (p.includes('datum=')) {
            crumbText = p.split("=").at(1)
          }
          
          breadcrumbs.push({
            path: p,
            to: this.$router.resolve({path: fullPath}).route,
            text: crumbText
          });
        }
      })
      return breadcrumbs;
    }
  }
};
</script>

<style scoped>
.q-breadcrumbs--last:not(:first-of-type) a{
  font-weight: bold;
}

a{
  color:white;
  font-size: 24px;
}

a:hover {color: white; text-decoration: underline;}
</style>
