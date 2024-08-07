
function setupAxios(csrftoken) {
    axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
}

axios.interceptors.response.use((response) => {
    return response;
}, async function (error) {
    console.log("Axios error", error) 
    let response = error.response
    let error_response = {
        status: response.status
    }
    
    if(response.status == 400) {
        error_response = {...error_response, ...response.data}
    } else if(response.status == 401){ 
        error_response.message = "Session expired. Please login again."
        setTimeout(() => {
            window.location.href = LOGOUT_URL
        }, 1100);
    } else { 
        error_response.message = response.statusText 
    } 
    return error_response
});



class APIRequest {

    formRequest(
        id, 
        extended_data, 
        processData=()=>{}, 
        checkValidation=()=>{return true}, 
        callback=()=>{}, 
        isMultiForm=false
    ){
        const class_self = this
        $(id).on('submit', async function(e){
            e.preventDefault();
            const self = this;
            let form_data;
            let process_data = processData();
            if(isMultiForm){
                form_data = new FormData($(self)[0]); 
                const extra_form_data = {
                    ...extended_data,
                    ...process_data
                } 
                Object.keys(extra_form_data).forEach(key_name => {
                    form_data.append(key_name, extra_form_data[key_name]);
                }) 

            } else {
                const $form = $(self);
                form_data = class_self.getFormDataJSON($form); 
                form_data = {
                    ...form_data,
                    ...extended_data,
                    ...process_data
                } 
            }
            
            if(checkValidation(class_self.getFormDataJSON($(self)))){
                let btn_html = $(self).find('button[type=submit]').eq(0).html()
    
                $(self).attr('disabled', true)
                $(self).find('button[type=submit]').eq(0).html('Please wait....')
                
                class_self.setupInputError('', false)  
                const response = await axios(
                    { 
                        url: $(this).attr('action'), 
                        method: $(this).attr('method'), 
                        data: form_data
                    }
                )
                
                if(response.status == 400){ 
                    $('.error-message').remove()
                    if(response.hasOwnProperty('message')){
                        $(self).prepend(`
                        <div class="error-message">
                            ${response.message}
                        </div>
                        `)
                    }

                    if(response.hasOwnProperty('error')){
                        Object.keys(response['error']).forEach(key_name => {
                            class_self.setupInputError(key_name, true, response['error'][key_name][0])  
                        });
                    }
                }
                callback(response) 
                $(self).attr('disabled', false)
                $(self).find('button[type=submit]').eq(0).html(btn_html) 
            }
            return false
        })
    }
    
    getFormDataJSON($form){
        var unindexed_array = $form.serializeArray();
        var indexed_array = {};
    
        $.map(unindexed_array, function(n, i){
            indexed_array[n['name']] = n['value'];
        });
    
        return indexed_array;
    }

    // For non-form post request
    // For small post body request like updating status, deletion etc
    // When making request make sure the data is ready and validated
    // For edit and creation form we can use the formRequest
    async makeRequest(
        url, 
        method,
        data, 
        processData=()=>{}, 
        callback=()=>{}, 
    ){
        
        let process_data = processData();
        const alldata = {
            ...data,
            ...process_data
        } 

        const response = await axios({
            method,
            url,
            data: alldata
          }); 
        callback(response) 
    }

    
    setupInputError(id, isShow=true, message=''){
        if(isShow){
            $(`.border-${id}`).addClass('error-border')
            $(`#message-${id}`).html(message)
        } else {
            $(`.border-${id}`).removeClass('error-border')
            $('.input-message-component').html('')
        }
    }

}

const API = new APIRequest();

