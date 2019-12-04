var mixin = {
    props: ['csrftoken'],
    delimiters: ['||', '||'],
    template: '' +
    '<form v-bind:action="action" v-on:input="input_event" v-on:submit.prevent="submit_event">' +
        '<template v-for="f in fields">'+
                '<div v-bind:class="fieldDivClassName(f)">'+ // div for field
                '<label v-if="!isHidden(f)">||f.label||</label>'+ // label
                    '<select v-if="isSelect(f)" v-bind:name="f.attrs.name" v-model="f.value">' +  // select
                    '<option v-for="c in f.choices">||c||</option>'+
                    '</select>'+
                    '<input v-else v-bind="f.attrs" v-model:value="f.value">'+ // input
                        '<template v-for="e in f.errors">'+ // errors
                            '<label v-if="!isHidden(f)" class="field_error" v-bind:id="e.code">||e.message||</label>'+
                        '</template>'+
               '</div>'+
            '</template>' +
        '<input v-if="csrftoken" type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrftoken">' +
        '<label v-for="e in non_fields_errors" class="non_field_error" v-bind:id="e.code">||e.message||</label>'+
        '<br>'+
        '<input type="submit">' +
    '</form>',
    methods: {
        autoCompleteHeaderKey: function(f) {return 'Auto-Complete'},
        isSelect: function(f) {return f.attrs.type == 'select'},
        isHidden: function(f) {return f.attrs.type == 'hidden'},
        hasErrors: function (f) {return f.errors.length > 0},
        fieldDivClassName: function(f){
            let obj = {};
            obj[f.attrs.name + '-form-wrap form-wrap'] = true;
            obj['has_error'] = this.hasErrors(f);
            return obj;
            },
        clearFieldsErrors: function () {for (let f in this.fields){this.fields[f].errors = [];}},
        submit_event: function () {
            this.makeRequest();
        },
        input_event: function(event){
            if (this.noReloadInputTypes.find(function (x) {return x === event.target.type})) {
                this.fields[event.target.name].errors = [];
            }
            else if (this.$attrs.autoreload !== undefined ){this.makeRequest(true)}
        },

        makeRequest: function(autocomplete){
            this.clearFieldsErrors();
            let r = new XMLHttpRequest(); let _this = this;
            r.onreadystatechange = function() {if (r.readyState === XMLHttpRequest.DONE) {_this.handleResponse(r)}};
            r.open(this.$el.method.toUpperCase(), this.$el.action);
            if (autocomplete){r.setRequestHeader(this.autoCompleteHeaderKey(), '1')}
            console.log(_this.autoCompleteHeaderKey);
            r.send(new FormData(this.$el));
        },
        handleResponse: function(r){
            if (r.status in this.responseHandlers){
                this.responseHandlers[r.status](this, r)} else {
                console.log('Unhandled response' + r)}
        },
    },
    data(){return {
        action: '',
        noReloadInputTypes: ['password'],
        non_fields_errors: [],
        responseHandlers: {
            422: function (vue, r) {let errors = JSON.parse(r.response);
                if (errors['__all__'] !== undefined){vue.non_fields_errors = errors['__all__']}
                for (let e in errors){if (e !== '__all__'){vue.fields[e].errors = errors[e];}}
            },
            200: function (vue, r) {
                let redirectUrl = vue.$attrs.successredirect;
                if (redirectUrl){window.location.href = redirectUrl}
                },
            204: function (vue) {}
        },
    }}
};