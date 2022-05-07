<template>
  <v-container>
    <v-row class="fill-height">
      <v-col>
        <request-workload-form />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import RequestWorkloadForm from '@/components/form/RequestWorkloadForm'
export default {
  components: {
    RequestWorkloadForm,
  },
  data() {
    return {}
  },
  computed: {},
  methods: {},
}
</script>
