function saved_files_load(parent_node){
    component_heading(parent_node, "h4", "Pre configured");
    component_select("saved", "files", parent_node, fetched_data.saved, true);
}

function saved_files_process(){
    el = document.getElementById('saved-files-select');
    file = el.value.replaceAll(' ', '_');
    return {"name":"3LinesFile", "file":`${file}`}
}

function img_files_load(parent_node){    
    component_heading(parent_node, "h4", "Images");
    component_select("saved", "images", parent_node, fetched_data.images, true);
}

function img_files_process(){
    el = document.getElementById('saved-images-select');
    file = el.value.replaceAll(' ', '_');
    return {"name":"Images", "file":`${file}`}
}

function animation_files_load(parent_node){
    component_heading(parent_node, "h4", "Animations");
    component_select("saved", "animation", parent_node, fetched_data.animations, true);
}

function animation_files_process(){
    el = document.getElementById('saved-animation-select');
    file = el.value.replaceAll(' ', '_');
    return {"name":"Animation", "directory":`${file}`}
}

function component_text(prefix, label, parent_node){
    const textElement = document.createElement("input");
    textElement.id = "{0}-text-input".replace('{0}',prefix); // Set an ID
    textElement.name = textElement.id; // Set a name for form submission
    parent_node.appendChild(textElement);
    parent_node.appendChild(document.createTextNode('  '+label));
}

function component_color(prefix, parent_node){
    component_select(prefix, "color", parent_node, Object.keys(fetched_data.colors), true);
    parent_node.appendChild(document.createTextNode('  colour'));
}

function component_speed(prefix, parent_node){
    //sleep speeds
    const optionsData = [
        { value: 0.005, text: "Really fast" },
        { value: 0.01, text: "Fast" },
        { value: 0.05, text: "Slow" },
        { value: 0.1, text: "Really Slow" }
    ];
    component_select(prefix, "speed", parent_node, optionsData, false);
    parent_node.appendChild(document.createTextNode('  speed'));
}

function component_time(prefix, parent_node){
    const optionsData = [
        { value: "0", text: "0 - forever" },
        { value: "5", text: "5" },
        { value: "10", text: "10" },
        { value: "15", text: "15" },
        { value: "30", text: "30" },
        { value: "60", text: "Hour" }
    ];
    component_select(prefix, "mins", parent_node, optionsData, false);
    parent_node.appendChild(document.createTextNode('  mins'));
}

function component_select(prefix, name, parent_node, options_data, simple, callback){
    const selectElement = document.createElement("select");
    selectElement.id = "{0}-{1}-select".replace('{0}',prefix).replace('{1}',name); // Set an ID
    selectElement.name = selectElement.id; // Set a name for form submission
    options_data.forEach(option_info => {
        const option = document.createElement("option");
        if (simple===false){
            option.value = option_info.value;
            option.textContent = option_info.text; // Use textContent for security and clarity
        } else {
            option.value = option_info;
            option.textContent = option_info; // Use textContent for security and clarity
        }
        selectElement.appendChild(option);
    });
    if (callback) {
        selectElement.addEventListener('change', function() {
            callback(selectElement.id, selectElement[selectElement.selectedIndex].value)
        });
    }
    parent_node.appendChild(selectElement);
}

function component_radio_buttons_callback(radio_buttons, radio, callback){    
    radio_buttons.forEach(button => {
        if (radio.value === button.btn.value){
            if (callback){
                callback(radio.value);
            }
        } else {
            button.btn.checked = false;
        }
    });
}

function component_radio_buttons(prefix, parent_node, value_label_arr, checked_value, callback) {
    //value_label_arr [{value:"10", text:"Ten"},{value:"20", text:"Twenty"}]
    //callback optional
    let all_radios = [];
    value_label_arr.forEach(radio => {
        const radioButton = document.createElement('input');
        radioButton.type = 'radio';
        radioButton.value = radio.value;
        radioButton.id = prefix + '-radio-' + radio.value;
        radioButton.name = radioButton.id
        radioButton.checked = false;
        if (radio.value === checked_value){radioButton.checked = true}

        const label = document.createElement('label');
        label.textContent = radio.text;
        all_radios.push({btn:radioButton, lbl:label});
    });
    all_radios.forEach(radio => {
        radio.btn.onclick = function() { 
            component_radio_buttons_callback(all_radios, radio.btn, callback);
        };        
        parent_node.appendChild(radio.btn);
        parent_node.appendChild(radio.lbl);
    });
}

function component_heading(parent_node, h, text){
    const heading = document.createElement(h);
    heading.textContent = text;
    parent_node.appendChild(heading);
}

function component_div(parent_node, id){
    const el = document.createElement("div");
    el.id = id;
    parent_node.appendChild(el);
    return el;
}

function check_str_int(str){
    const num = parseInt(str);
    if (!isNaN(num) && Number.isInteger(num)) {
        return true;
    } else {
        return false;
    }
}