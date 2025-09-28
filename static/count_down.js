function count_down_load(parent_node){
    const prefix = 'count-down';
    const label = 'Minutes';
    component_heading(parent_node, "h4", "Count Down");
    component_color(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix,label,parent_node);
}

function count_down_process(){
    const colour = document.getElementById('count-down-color-select');
    const display_text = document.getElementById('count-down-text-input');
    display_text.value = display_text.value.trim();
    mins_to_countdown = parseInt(display_text.value);
    if (display_text.value==='' || !Number.isInteger(mins_to_countdown)){throw "You must enter a whole number"}
    return {"name":"CountDown", "mins":0, "color":colour.value, "mins_to_countdown":mins_to_countdown}
}