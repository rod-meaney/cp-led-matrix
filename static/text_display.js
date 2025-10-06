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
                console.log('This is a problem!');
        }
    }
    return req;
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
    component_select(prefix, "city", parent_node, Object.keys(fetched_data.cities).toSorted(), true);
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