//config
$float_speed=1500; //milliseconds
$float_easing="easeOutQuint";
$menu_fade_speed=500; //milliseconds
$closed_menu_opacity=1;

//cache vars
$fl_menu_hover=$("#fl_menu_hover");
$fl_menu=$("#fl_menu");
$fl_menu_menu=$("#fl_menu .menu");
$fl_menu_label=$("#fl_menu .label");
$fl_menu_items=$(".menu_item");

function initializeMenu() {
    menuPosition=$('#fl_menu').position().top;
    var in_menu = false;
    var in_hover = false;
    var showing_menu = false;
    var timeout_id = 0;
    function show_menu() {
	if (showing_menu)
	    return;
	showing_menu = true;
	$fl_menu_label.fadeTo($menu_fade_speed, 1);
	$fl_menu_menu.fadeIn($menu_fade_speed);
    }
    function hide_menu() {
	if (in_menu || in_hover)
	    return;
	showing_menu = false;
	$fl_menu_label.fadeTo($menu_fade_speed, $closed_menu_opacity);
	$fl_menu_menu.fadeOut($menu_fade_speed);
    }
    $fl_menu.hover(
	function(){ //mouse over
	    in_menu = true;
	    clearTimeout(timeout_id);
	    show_menu();
	},
	function(){ //mouse out
	    in_menu = false;
	    var id = setTimeout(hide_menu, 50);
	    timeout_id = id;
	}
    );
    $fl_menu_hover.hover(
	function(){ //mouse over
	    in_hover = true;
	    clearTimeout(timeout_id);
	    show_menu();
	},
	function(){ //mouse out
	    in_hover = false;
	    var id = setTimeout(hide_menu, 50);
	    timeout_id = id;
	}
    );
}

$(window).load(initializeMenu);
