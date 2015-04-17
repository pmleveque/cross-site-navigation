/*global document, window, jq1112 */

var jq1112 = jq1112 || jQuery;

(function($){


// Menu plugin
// © PM Leveque 2010 & Isa 2015
jQuery.fn.extend({
    cef_nav_menu: function() {
        var menus = $(this);

        var closetimer  = null;
        var active_menu = null;
        var timeout     = 200;

        var close_all_menus = function() {
            active_menu = null;
            menus.each(function(){$(this).fadeOut(50);});
        };

        var start_timer = function() {
            if (active_menu) {
                closetimer = window.setTimeout(close_all_menus, timeout);
            }
        };

        var cancel_timer = function() {
            if (closetimer) {
                window.clearTimeout(closetimer);
                closetimer = null;
            }
        };

        //Iterate over the current set of matched elements
        return this.each(function(){
            var menu = $(this);
            var menu_title = menu.prev("a");

            var menu_show = function(){
                cancel_timer();
                if (active_menu !== menu) {
                    close_all_menus();
                }
                active_menu = menu;
                menu.css('left', menu_title.offset().left - 6);
                menu.show();
            };

            menu_title.click(function(){
                if (active_menu) {
                    close_all_menus();
                    }else{
                    menu_show();
                }
                return false;
            });
            menu_title.mouseover(function(){
                if (active_menu) {
                    menu_show();
                }
            });
            menu.mouseout(start_timer);
            menu.mouseover(cancel_timer);

        });
    }
});


// CEF navigation bar
// © Pierre-Marie Lévêque
// L'affichage des résultats doit respecter les règles de Google:
// Guidelines for implementing Google™ Custom Search
// http://www.google.com/cse/docs/branding.html

var api_host = "{{host}}";
window.CEF = {};
var CEF = window.CEF;

CEF.settings = {
    site_search: {% ifequal navbar.cse_unique_id "recherche.catholique.fr" %}false{% else %}true{% endifequal %},
    share_links: true,
    google_search_restriction: {% if not navbar.cse_unique_id %}location.host{% else %}"{{ navbar.cse_unique_id }}"{% endif %},
    scrolling_bar: true,
    image_search_results: true,
    news_search_results: true
}

CEF.settings.google_search_restriction_label = "Pages de " + CEF.settings.google_search_restriction;

CEF.navigationBarHtml = "{{navbar_template|safe}}";
CEF.searchResultsHtmlTemplate = "{{search_results_template|safe}}";

// Function utilitaire
CEF.import_style = function (src){
    jQuery('head').append('<link rel="stylesheet" href="http://' + api_host + '/stylesheets/' + src + '" type="text/css" media="all" />');
}

CEF.localSearch = function() {
    // On active la recherche locale
    this.import_style("site_search.1-0-2.css");
    $("body").append(this.searchResultsHtmlTemplate);
    $("#cef_search_floatbox, #cef_search_floatbox_bg").hide();
    var cx = this.settings.google_search_restriction;
    var e = document.createElement('script');
    e.type = 'text/javascript'; e.async = true;
    e.src = (document.location.protocol == 'https' ? 'https:' : 'http:') +
        '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(e, s);

    // clicka
    $("#cef_search").submit(function(){
        var query = $("#site_search").attr("value");
        CEF.search(query);
        return false;
    });
    // links
    $("#cef_more_result_links a").click(function() {
        var query = $("#site_search").attr("value");
        var link = $(this).attr('href').replace('q=', 'q=' + encodeURI(query));
        window.location.href = link;
        return false;
    });

    // close search
    $('.remove_cef_search_floatbox').click(function() {
        $("#cef_search_floatbox, #cef_search_floatbox_bg").hide();
    });
}

// Triggers search event
CEF.search = function(query) {

    $('.gsc-search-box').hide();
    $('.gsc-input').val(query);
    $('.gsc-search-button').click();
    $('.cef_query').text(query);

    window.scrollTo(0,0);

    // Problèmes avec IE
    if ($.browser.msie) {
        $("#cef_search_floatbox_bg").css("background-color", "transparent");
    }

    // show search. everything is handle by gcse
    $("#cef_search_floatbox, #cef_search_floatbox_bg").show();

    // Google Analytics tracking
    if(typeof(pageTracker)!='undefined'){
        pageTracker._trackPageview('/?search_query=' + query);
    }
}


CEF.initNavigationBar = function(options){
    // Les options par défaut sont configurées dans la variable CEF.settings
    if (typeof(options) != 'undefined'){
        $.extend(CEF.settings, options);
    }

    // On désactive la recherche intégrée si l'API google n'a pas été initialisée
    if (typeof(google) == 'undefined'){
        $.extend(CEF.settings, {site_search: false});
    }

    // On ajoute le code HTML de la barre de navigation à l'élément #cef-root (ou sinon à <body>)
    if ($("#cef-root").length) {
        $("#cef-root").append(CEF.navigationBarHtml);
    }else{
        $("body").append(CEF.navigationBarHtml);
    }

    // On importe la feuille de style
    // La barre de navigation ne s'affiche qu'une fois cette feuille de style chargée.
    CEF.import_style("navigation_bar.2-0.css");

    // On active le fonctionnement des menus
    $("div.cef_nav_menu").cef_nav_menu();

    // On supprime les liens de partage si nécessaire
    if (!CEF.settings.share_links) {
        $("#cef_navigation_links_right").remove();
    }

    // La barre de navigation est "fixée" si demandé
    if (CEF.settings.scrolling_bar) {
        $("#cef_navigation").css({position: "fixed"});
    }


    // On active la recherche interne si demandé
    if (CEF.settings.site_search) {
        // On active la recherche locale
        $('#site_search').attr('placeholder','recherche dans ce site');
        CEF.localSearch();
    }else{
        $('#site_search').attr('placeholder','recherche sites catholiques');
    }

}

$(window).load(function(){
    $('#search_input_id').submit(function(){
        $("#site_search").attr("value", "");
        return false;
    });
});

if (window.cefAsyncInit) {
    cefAsyncInit();
}else{
    // Si la fonction d'initialisation asynchrone n'existe pas, on charge le script une fois la page "ready":
    $(function(){
        CEF.initNavigationBar();
    });
};

})(jq1112);
