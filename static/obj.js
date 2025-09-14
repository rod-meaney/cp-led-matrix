function saved_files_load(parent_node){
    component_heading(parent_node, "h4", "Pre configured");
    component_select("saved", "files", parent_node, fetched_data.saved, true);
}

function saved_files_process(){
    el = document.getElementById('saved-files-select');
    file = el.value.replaceAll(' ', '_');
    return './loadsaved?file={0}&type=saved'.replace('{0}',file);
}

function img_files_load(parent_node){    
    component_heading(parent_node, "h4", "Images");
    component_select("saved", "images", parent_node, fetched_data.images, true);
}

function img_files_process(){
    el = document.getElementById('saved-images-select');
    file = el.value.replaceAll(' ', '_');
    return './loadsaved?file={0}&type=img'.replace('{0}',file);
}

function animation_files_load(parent_node){
    component_heading(parent_node, "h4", "Animations");
    component_select("saved", "animation", parent_node, fetched_data.animations, true);
}

function animation_files_process(){
    el = document.getElementById('saved-animation-select');
    file = el.value.replaceAll(' ', '_');
    return './loadsaved?file={0}&type=animation'.replace('{0}',file);
}

function text_display_load(parent_node){
    //CHoosing lines
    let initial_line = 1
    let prefix = 'text-display';
    component_heading(parent_node, "h4", "Text Display");
    component_time(prefix, parent_node)
    parent_node.appendChild(document.createElement("p"));
    let buttons = [{value:1,text:"1 row"},{value:2,text:"2 rows"},{value:3,text:"3 rows"}];
    component_radio_buttons(prefix, parent_node, buttons, initial_line, text_display_update_lines);

    let var_lines = prefix + '-var'; //dive
    component_div(parent_node,var_lines);
    text_display_update_lines(initial_line);
}

function text_display_process(){
    //really simple way to now how many lines
    let req = {"name":"ThreeLines", "lines":[], "mins":document.getElementById("text-display-mins-select").value}
    let checked=1;
    if (document.getElementById("text-display-radio-2").checked){checked=2};
    if (document.getElementById("text-display-radio-3").checked){checked=3};
    for (let i = 1; i <= checked; i++) {
        switch (document.getElementById("text-display-line-"+i+"-select").value) {
            case "--Select one--":
                throw("You need to make a selection for line "+i);
            case "Tram":
                const tram_route = document.getElementById(`text-display-component-${i}-route-text-input`);
                const tram_stop_id = document.getElementById(`text-display-component-${i}-stop-id-text-input`);
                tram_route.value = tram_route.value.trim();
                tram_stop_id.value = tram_stop_id.value.trim();
                if (check_str_int(tram_route.value) && check_str_int(tram_stop_id.value)){
                        req["lines"].push({"type":"tram", "data":{"stopNo":`${tram_stop_id.value}`, "routeNo":`${tram_route.value}`}})
                } else {
                    throw "Route and Stop id must be whole numbers";
                }
                break;
            case "Text":
                const text_color = document.getElementById(`text-display-component-${i}-color-select`).value;
                const text_text = document.getElementById(`text-display-component-${i}-text-input`);
                text_text.value = text_text.value.trim();
                req["lines"].push({"type":"text", "color":text_color, "text":text_text.value,"data":{}});
                break;
            case "Scrolling":
                const scroll_color = document.getElementById(`text-display-component-${i}-color-select`).value;
                const scroll_text = document.getElementById(`text-display-component-${i}-text-input`);
                scroll_text.value = scroll_text.value.trim();
                let scroll_type = "scroll";
                if (document.getElementById(`text-display-component-${i}-radio-reverse`).checked){scroll_type = "reverse_scroll";}
                if (scroll_text.value==""){
                    throw "Enter some text for the scroll";
                } else {
                    req["lines"].push({"type":scroll_type, "color":scroll_color ,"text":scroll_text.value, "data":{}});
                }
                break;
            case "Weather":
                const weather_color = document.getElementById(`text-display-component-${i}-color-select`).value;
                const weather_city = document.getElementById(`text-display-component-${i}-city-select`).value;
                req["lines"].push({"type":"weather", "color":weather_color, "data":{"city":weather_city}});
                break;
            case "Time":
                const time_color = document.getElementById(`text-display-component-${i}-color-select`).value;
                let time_seconds = false;
                if (document.getElementById(`text-display-component-${i}-radio-yes`).checked){time_seconds = true;}
                req["lines"].push({"type":"clock", "color":time_color, "data":{"seconds":time_seconds}});
                break;
            default:
                console.log('This is a problem!')
        }
    }
    const jsonString = JSON.stringify(req);
    const encodedJsonString = encodeURIComponent(jsonString);
    return "./loadjson?json=" + encodedJsonString;
}

function text_display_update_lines(selected_value){
    let prefix = 'text-display';
    let var_lines_parent = document.getElementById(prefix + '-var');
    var_lines_parent.innerHTML = '';
    text_display_line_load(prefix, var_lines_parent, selected_value);
}

function text_display_line_load(prefix,parent_node,lines){
    const line_options = ["--Select one--", "Text","Time","Tram","Scrolling","Weather"];
    for (let i = 1; i <= lines; i++) {
        component_heading(parent_node, "h5", "Line "+i);
        component_select(prefix, "line-"+i, parent_node, line_options, true, text_display_choice_load);
        component_div(parent_node,'text-display-component-'+i);
    }
}

function text_display_choice_load(id, choice){
    let row = id.split("-")[3];
    let prefix = 'text-display-component-'+row;
    let parent_node = document.getElementById(prefix)
    parent_node.innerHTML = '';
    let smooth_choice = choice.replaceAll(" ", "_").toLowerCase();
    let funtion_name = "text_display_{0}_load".replace('{0}', smooth_choice)
    
    window[funtion_name](prefix, parent_node); //Loads dynamic html
}

function text_display_time_load(prefix, parent_node){
    parent_node.appendChild(document.createElement("p"));
    component_color(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    parent_node.appendChild(document.createTextNode('seconds '));
    let buttons = [{value:"yes",text:"yes"}, {value:"no",text:"no"}];
    component_radio_buttons(prefix, parent_node, buttons, "no");
}

function text_display_weather_load(prefix, parent_node){
    parent_node.appendChild(document.createElement("p"));
    component_select(prefix, "city", parent_node, Object.keys(fetched_data.cities), true);
    parent_node.appendChild(document.createElement("p"));
    component_color(prefix,parent_node);
}

function text_display_scrolling_load(prefix, parent_node){
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix,"  Text",parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_color(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    let buttons = [{value:"right_to_left",text:"right to left"}, {value:"reverse",text:"reverse"}];
    component_radio_buttons(prefix, parent_node, buttons, "right_to_left");
}

function text_display_text_load(prefix, parent_node){
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix,"  Text",parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_color(prefix,parent_node);
}

function text_display_tram_load(prefix, parent_node){
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix+"-route","  Route",parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix+"-stop-id","  Stop id (NOT number)",parent_node);    
}

function word_punch_load(parent_node){
    let prefix = 'word-punch';
    let label = 'Sentence';
    component_heading(parent_node, "h4", "Word Punch");
    component_time(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_color(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix,label,parent_node);
}

function word_punch_process(){
    const colour = document.getElementById('word-punch-color-select');
    const time = document.getElementById('word-punch-mins-select');
    const display_text = document.getElementById('word-punch-text-input');
    display_text.value = display_text.value.trim();
    if (display_text.value===''){throw "Please enter a sentence."}
    let jsonobj = {"name":"WordPunch", "mins":time.value, "color":colour.value, "sentence":display_text.value, "sleep":0.005}
    const jsonString = JSON.stringify(jsonobj);
    const encodedJsonString = encodeURIComponent(jsonString);
    return "./loadjson?json=" + encodedJsonString;
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