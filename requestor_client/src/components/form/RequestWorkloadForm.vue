<template>
  <v-card tile>
    <v-card-title>Request Workload Processing</v-card-title>
    <v-divider />
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
          v-model="formModel.name"
          outlined
          :label="form.name.label"
          :placeholder="form.name.placeholder"
          required
          :rules="form.name.rules"
        />
        <v-combobox
          v-model="formModel.machineType"
          outlined
          :label="form.machineType.label"
          :placeholder="form.machineType.placeholder"
          :rules="form.machineType.rules"
          :items="machineTypes"
          required
        />
        <v-file-input
          v-model="formModel.artefact"
          outlined
          :label="form.artefact.label"
          :placeholder="form.artefact.placeholder"
          required
          counter
          show-size
          :rules="form.artefact.rules"
        />
        <v-subheader class="pl-0 mt-3">YAML Configuration</v-subheader>
        <prism-editor class="my-editor" v-model="code" :highlight="highlighter" line-numbers></prism-editor>

        <v-editor></v-editor>
      </v-form>
    </v-card-text>
    <v-divider class="mt-5"></v-divider>
    <v-card-actions>
      <v-btn text @click="handleCancelForm">Cancel</v-btn>
      <v-spacer />
      <v-btn tile color="primary" @click="handleSubmitForm">Submit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
// import Prism Editor
import { PrismEditor } from 'vue-prism-editor'
import 'vue-prism-editor/dist/prismeditor.min.css' // import the styles somewhere

// import highlighting library (you can use any library you want just return html string)
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-javascript'
import 'prismjs/themes/prism-tomorrow.css' // import syntax highlighting styles

export default {
  components: {
    PrismEditor,
  },
  data: () => ({
    machineTypes: ['Data Science L2', 'Data Science L3', 'Graphic Processing L2', 'Graphic Processing L3'],
    valid: true,
    formModel: {
      name: null,
      email: null,
      address: null,
      city: null,
      state: null,
      zip: null,
      country: null,
    },
    code: 'console.log("Hello World")',
    form: {
      name: {
        label: 'Workload Name',
        placeholder: 'Workload Name',
        rules: [(v) => !!v || 'This field is required'],
      },
      machineType: {
        label: 'Machine Type',
        placeholder: 'Machine Type',
        rules: [(v) => !!v || 'This field is required'],
      },
      artefact: {
        label: 'Artefact File',
        placeholder: 'Artefact File',
        rules: [(v) => !!v || 'This field is required'],
      },
    },
    formHasErrors: false,
  }),
  methods: {
    handleCancelForm() {
      this.$refs.form.reset()
    },
    handleSubmitForm() {
      if (this.$refs.form.validate()) {
        console.log('handle form process logic here')
      }
    },
    highlighter(code) {
      return highlight(code, languages.js) // languages.<insert language> to return html with markup
    },
  },
}
</script>
