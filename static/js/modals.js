$.fn.loadModal = function(options){
    var _modal = this;
    var _modal_dialog = _modal.find("#modal_dialog");
    var _modal_content = _modal.find(".modal-content");
 
    
    var settings = $.extend({
        url: "",
        params: {},
        size: "",
        centered: true,
        show_loading: true,
        callback: function(){},
        icon: "fa-spinner",
        text: "Currently loading content, please wait a sec...",
        is_priority: false,
    }, options );

    const params_url = new URLSearchParams(settings.params).toString();

    var loader =
        "<div style='display:flex; align-items:center; height:100%; padding:3em;'>"+
            "<div style='width:100%; text-align:center; display:inline-block;'>"+
                "<div style='color:#676767; font-size:14px;'>"+
                    "<i class='fas "+settings.icon+" fa-spin fa-fw'></i>"+
                "</div>"+
                "<div style='color:#9a9a9a; font-size:12px;'>"+settings.text+"</div>"+
            "</div>"+
        "</div>";

    if(settings.url != ""){
        var dialog_class = "modal-dialog "+settings.size;

        if(settings.show_loading)
            _modal_content.html(loader);

        if(settings.centered)
            dialog_class += " modal-dialog-centered";

        if(settings.is_priority)
            _modal.addClass("priority");

        _modal_dialog.attr("class", dialog_class);
        _modal.modal("show");
        let params_string = '';
        if(!settings.url.includes('?')){
            params_string = '?'
        } else if(params_url.trim() != '') {
            params_string = '&'
        }

        _modal_content.load(settings.url+params_string+params_url);
    }

    settings.callback();
};

$(function(){
    $(document).on("click", "[data-open-modal]", function(e){
        e.preventDefault(); 
        var url = $(this).attr("data-modal-url") || $(this).attr("href");  
        var params = {};
        var size = $(this).attr("data-modal-size") || "modal-lg";
        var type = $(this).attr("data-modal-type") || "modal_rounded";
        /**
         * Modal type
         * modal_rounded
         * modal_general
         */
        var is_priority = $(this).attr("data-priority") || false; 
        $("#"+type).loadModal({
            url: url,
            params:params,
            size: size,
            is_priority: is_priority,
        });
    });
    
});


const openNewModal = (modalObject) => {
    // modalObject -> JSON Object
    // Variable keys
    // - url:string 
    // - params: {}
    // - type: modal_general || modal_rounded
    // - size
    // - priority: true || false
    
    var valuesObj = { ...modalObject }
    $("#"+(valuesObj.type || "modal_rounded")).loadModal({
        url: valuesObj.url,
        params: valuesObj.params || {},
        size: valuesObj.size || "modal-lg",
        is_priority: valuesObj.priority  || false,
    });
}

