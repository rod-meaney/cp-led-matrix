function halloween_load(parent_node){
    const prefix = 'halloween';    
    component_heading(parent_node, "h4", "Halloween");
    component_time(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
}

function halloween_process(){
    const time = document.getElementById('halloween-mins-select');
    return {"name":"Halloween", "mins":time.value}
}