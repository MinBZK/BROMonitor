<template>
    <div class="col-12">
        <div class="source" :style="alignment()" v-for="source in filteredSources" :key="source.name">
            Bron: {{ source.name.toUpperCase() }},
            <div v-if="source.types.length > 1">
                <div class="type" :style="alignment()"  v-for="type in source.types" :key="type.type"> 
                 {{ type.type.toUpperCase() }},  {{ parseDate(type.updated) }} 
                </div>
            </div>
            <span v-else>
                <span class="type" :style="alignment()"  v-for="type in source.types" :key="type.type"> 
                {{ parseDate(type.updated) }} 
                </span>
            </span>
        </div>
    </div>
</template>

<script lang="ts">
import { SourceModel, SourceTypeModel } from "@/models/source.ts";
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
    props: {
        sources: {
            type: Array as () => SourceModel[]
        },
        rightAlign: {
            type: Boolean,
            default: false
        }
    },
    methods:{
        parseDate(updated){
            if(updated != null)
            {
                const options = {timeZone: 'Europe/Amsterdam', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(updated).toLocaleString('nl-NL', options);
            }
            else
            {
                return "ophaaldatum onbekend"
            }
        },
        alignment(){
            return this.$props.rightAlign ? "text-align: right;" : "text-align: left;";
        }
    },
    computed: {
        filteredSources: function(): SourceModel[]
        {
            // Reduce the list of types in a source to a single element if all the dates are the same
            const output = (this.sources as SourceModel[])
            for(const source of (output)){
                const sameDates = (s: SourceModel) => s.types.every((t: SourceTypeModel) => t.updated === s.types[0].updated)
                if(sameDates(source)){
                    source.types = [source.types[0]]
                }
            }
            return output
        }
    }
});
</script>

<style scoped>
.source {
    font-style: italic;
    font-size: 0.95rem;
}

.type {
    font-style: italic;
    font-size: 0.95rem;
}
</style>