$.fn.loadSubpage = function(options){
    var _obj = this;

    var settings = $.extend({
        url: "",
        show_loading: true,
        pre_load: function(elem){},
        callback: function(){},
        icon: "fa-spinner",
        text: "Currently loading content, please wait a sec...",
        is_table_column: false
    }, options );

    var loader =
        "<div style='display:flex; align-items:center; height:100%; padding:3em;'>"+
            "<div style='width:100%; text-align:center; display:inline-block;'>"+
                "<div style='color:#676767; font-size:14px;'>"+
                    "<i class='fas "+settings.icon+" fa-spin fa-fw'></i>"+
                "</div>"+
                "<div style='color:#9a9a9a; font-size:12px;'>"+settings.text+"</div>"+
            "</div>"+
        "</div>";
    if(settings.is_table_column){
        loader =
        `
        <td colspan="${settings.is_table_column}">
            <div style='display:flex; align-items:center; height:100%; padding:3em;'>
                <div style='width:100%; text-align:center; display:inline-block;'>
                    <div style='color:#676767; font-size:14px;'>
                        <i class='fas ${settings.icon} fa-spin fa-fw'></i>
                    </div>
                    <div style='color:#9a9a9a; font-size:12px;'>${settings.text}</div>
                </div>
            </div>
        </td>
        `
        ;
    }

    if(settings.url != ""){
        if(settings.show_loading)
            _obj.html(loader);

        settings.pre_load(_obj);

        _obj.load(settings.url, function(){
            settings.callback();
        });
    }
};


function urlParameterize(data){
    params = []
    $.each(data, function (key, value) {
        params.push(key+"="+value)
    });

    return encodeURI(params.join("&"))
}



var debounced = function(delay, fn) {
    let timerId;

    return function (...args) {
        if (timerId) {
            clearTimeout(timerId);
        }
        timerId = setTimeout(() => {
            fn(...args);
            timerId = null;
        }, delay);
    }
}

var formatCurrency = function(amount){
    return amount.toLocaleString('en-US', {style: 'currency', currency: 'PHP'});
}

var commafy = function(amount, hasDecimal=true){
    var options = {}
    
    if (hasDecimal){
        options = {
            style: 'decimal',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        };
    }
    return amount.toLocaleString(undefined, options);
}

function setInputReadOnly(input_names, isReadOnly, clearValues) {
    input_names.forEach((item, index) => {
        let name = `input[name="${item}"]`
        if($(name).length) {
            $(name).prop('readonly', isReadOnly);
        }
        else {
            name = `select[name="${item}"]`
            $(`select[name="${item}"]`).prop('disabled', isReadOnly);
        }
        
        
        if(clearValues){
            $(name).val('')
        }
    })
}


function showToast(message) {
    $('body').prepend('<div id="snackbar"></div>')
    setTimeout(() => {
        var x = document.getElementById("snackbar");
        x.innerHTML = message
        x.className = "show";
        setTimeout(function(){ 
            x.className = x.className.replace("show", ""); 
            setTimeout(() => {
                $('#snackbar').remove()
            }, 400);
        }, 1000);
    }, 500);
} 

function copyToClipboard(text) {
    const input = document.createElement('input');
    input.style.position = 'fixed';
    input.style.opacity = 0;
    input.value = text;
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
}


function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
    }
    return result;
}


function downloadTextFile(filename, text) {
    var element = document.createElement('a');
    text = window.atob(text)
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
}