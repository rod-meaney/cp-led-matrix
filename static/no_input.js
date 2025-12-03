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

function eightball_load(parent_node){
    const prefix = 'eightball';
    component_heading(parent_node, "h4", "Ask your question aloud");
    component_time(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
	//Default it go for 5 mins max
	document.getElementById('eightball-mins-select').value = 5; 
}

function eightball_process(){
    const time = document.getElementById('eightball-mins-select');
    return {"name":"Eightball", "mins":time.value}
}