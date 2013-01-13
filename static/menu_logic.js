//config
$float_speed=1500; //milliseconds
$float_easing="easeOutQuint";
$menu_fade_speed=500; //milliseconds
$closed_menu_opacity=0.75;

//cache vars
$fl_menu=$("#fl_menu");
$fl_menu_menu=$("#fl_menu .menu");
$fl_menu_label=$("#fl_menu .label");

function initializeMenu() {
    menuPosition=$('#fl_menu').position().top;
    $fl_menu.hover(
	function(){ //mouse over
	    $fl_menu_label.fadeTo($menu_fade_speed, 1);
	    $fl_menu_menu.fadeIn($menu_fade_speed);
	},
	function(){ //mouse out
	    $fl_menu_label.fadeTo($menu_fade_speed, $closed_menu_opacity);
	    $fl_menu_menu.fadeOut($menu_fade_speed);
	}
    );
}

$(window).load(initializeMenu);
