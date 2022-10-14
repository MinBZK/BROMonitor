<template>
    <div class="markdown-body" v-html="fileContent"></div>
</template>

<script>
import { defineComponent } from "@vue/composition-api";
import showdown from "showdown";

export default defineComponent({
    props: {
        data: String
    },
    setup(){
        showdown.setFlavor('github');
        // Custom showdown extension, adding target="_blank" to all converted links/anchors.
        showdown.extension('targetLink', function() {
            return [{
                type: 'lang',
                regex: /[!]{0,1}\[((?:\[[^\]]*]|[^[\]])*)]\([ \t]*<?(.*?(?:\(.*?\).*?)?)>?[ \t]*((['"])(.*?)\4[ \t]*)?\)/g,
                replace: function(wholematch, linkText, url, a, b, title, c) {
                
                // We matched an image and should do nothing with it
                if(wholematch.charAt(0) == "!") return wholematch

                let result = '<a href="' + url + '"';
                if (typeof title != 'undefined' && title !== '' && title !== null) {
                    title = title.replace(/"/g, '&quot;');
                    title = showdown.helper.escapeCharacters(title, '*_', false);
                    result += ' title="' + title + '"';
                }
                
                // Do not add target blank for local reference links
                if(url.charAt(0) != '#') result += ' target="_blank"';
                
                result += '>' + linkText + '</a>';

                return result;
                }
            }];
        });
    },
    data() {
        const fileContent = "";
        const converter = new showdown.Converter({ extensions: ['targetLink'] });
        return {
            fileContent, converter
        }
    },
    created: function() {
        this.fileContent = this.converter.makeHtml(this.$props.data);
    },
    watch: { 
      	data: function(newVal, oldVal) {
            this.fileContent = this.converter.makeHtml(newVal);
        }
    }
});
</script>