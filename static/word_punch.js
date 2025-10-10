function word_punch_load(parent_node){
    let prefix = 'word-punch';
    let label = 'Sentence';
    component_heading(parent_node, "h4", "Word Punch");
    component_time(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_color(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix,label,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_speed(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    let buttons = [{value:"standard",text:"standard"}, {value:"big",text:"big"}];
    component_radio_buttons(prefix, parent_node, buttons, "standard");
}

function word_punch_process(){
    const colour = document.getElementById('word-punch-color-select');
    const time = document.getElementById('word-punch-mins-select');
    const display_text = document.getElementById('word-punch-text-input');
    const speed = document.getElementById('word-punch-speed-select');
    display_text.value = display_text.value.trim();
    let big = false;
    if (document.getElementById('word-punch-radio-big').checked){big = true;}

    if (display_text.value===''){throw "Please enter a sentence."}
    return {"name":"WordPunch", "mins":time.value, "color":colour.value, "sentence":display_text.value, "sleep":speed.value, "big":big}
}