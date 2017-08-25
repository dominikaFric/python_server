$(document).ready(function(){
    var ajaxData;
    var menuBars;
    var screens;
    var menus;

    var url="http://127.0.0.1:8088/";

    loadResources();

    

    function loadResources(){
        ajaxRequest("/api/menu-bars","GET").done(function(){
            menuBars=ajaxData;
            console.log(ajaxData);
        });

        ajaxRequest("/api/screens","GET").done(function(){
            screens=ajaxData;
            console.log(ajaxData);
        });

        ajaxRequest("/api/menus","GET").done(function(){
            menus=ajaxData;
            console.log(ajaxData);
        });
    }



    function ajaxRequest(path,requestType, dataToSend){
        var d = $.Deferred();
            $.ajax({
                url:"http://localhost:8088"+path,
                data:dataToSend,
                type:requestType,
                contentType:"application/json",
                success:function(data){
                    ajaxData=data;
                    d.resolve();
                },
                error:function(data){
                    d.reject();
                }
            });
        return d.promise();
    }
});