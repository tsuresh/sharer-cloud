<template>
  <div class="form-elements">
    <div class="row">
      <div class="flex xs12">
        <va-card :title="$t('forms.inputs.title')">
          <va-card-content>
            <form>
              <div class="row">
                <div class="flex md4 sm6 xs12">
                  <va-input v-model="simple" placeholder="Text Input" />
                </div>
                <div class="flex md4 sm6 xs12">
                  <va-input v-model="withIcon" placeholder="Input With Icon">
                    <template #prepend>
                      <va-icon color="gray" name="envelope" />
                    </template>
                  </va-input>
                </div>
                <div class="flex md4 sm6 xs12">
                  <va-input
                    v-model="withButton"
                    placeholder="Input With Button"
                  >
                    <template #append>
                      <va-button style="margin-right: 0" small>
                        UPLOAD
                      </va-button>
                    </template>
                  </va-input>
                </div>
                <div class="flex md4 sm6 xs12">
                  <va-input
                    v-model="successfulEmail"
                    type="email"
                    label="Email (Validated with success)"
                    success
                  >
                  </va-input>
                </div>
                <div class="flex md4 sm6 xs12">
                  <va-input
                    v-model="clearableText"
                    placeholder="Input With Clear Button"
                    removable
                  />
                </div>
                <div class="flex md4 sm6 xs12">
                  <va-input
                    v-model="wrongEmail"
                    type="email"
                    label="Email (Validated)"
                    error
                    :error-messages="errorMessages"
                  >
                  </va-input>
                </div>
                <div class="flex md4 sm6 xs12">
                  <va-input
                    v-model="withDescription"
                    placeholder="Text Input (with description)"
                    :messages="messages"
                  />
                </div>
              </div>
            </form>
          </va-card-content>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>
import CountriesList from '../data/CountriesList'

export default {
  name: 'form-elements',
  data () {
    return {
      isMale: true,
      countriesList: CountriesList,
      chosenCountry: '',
      simple: '',
      withIcon: '',
      withButton: '',
      withDescription: '',
      clearableText: 'Vasili Savitski',
      successfulEmail: 'andrei@dreamsupport.io',
      wrongEmail: 'andrei@dreamsupport',
      messages: ['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ' +
        'incididunt ut labore et dolore magna aliqua.'],
      errorMessages: ['Field should contain a valid email'],
      simpleOptions: [
        {
          id: 1,
          description: 'First option',
        },
        {
          id: 2,
          description: 'Second option',
        },
        {
          id: 3,
          description: 'Third option',
        },
      ],
      simpleSelectModel: '',
      multiSelectModel: [],
      multiSelectCountriesModel: [],
      searchableSelectModel: '',
      multiSearchableSelectModel: [],
      radioSelectedOption: 'option1',
      radioSelectedDisableOption: 'option1',
      checkbox: {
        unselected: false,
        selected: true,
        readonly: true,
        disabled: true,
        error: false,
        errorMessages: true,
      },
      toggles: {
        unselected: false,
        selected: true,
        disabled: true,
        small: false,
        large: false,
      },
      datepicker: {
        simple: '2018-05-09',
        time: '2018-05-08 14:10',
        range: '2018-05-08 to 2018-05-23',
        disabled: '2018-05-09',
        multiple: '2018-04-25, 2018-04-27',
        customFirstDay: '2018-05-09',
        customDate: '2017-Dec-06',
      },
    }
  },
  methods: {
    clear (field) {
      this[field] = ''
    },
  },
}
</script>

<style>
  .row.row-inside {
    max-width: none;
  }

  .va-input-wrapper, fieldset {
    margin-bottom: 0.5rem;
  }
</style>
