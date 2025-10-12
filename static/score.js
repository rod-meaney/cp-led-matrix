function score_load(parent_node){
    const prefix = 'score';
    component_heading(parent_node, "h4", "Score");
    
    component_text(`${prefix}-c1`,"",parent_node);
    document.getElementById(`${prefix}-c1-text-input`).value = 0;
    component_button(parent_node, "T1 +", addToTeam1);
    component_button(parent_node, "-", subtractFromTeam1);
    parent_node.appendChild(document.createElement("p"));

    component_text(`${prefix}-c2`,"",parent_node);
    document.getElementById(`${prefix}-c2-text-input`).value = 0;
    component_button(parent_node, "T2 +", addToTeam2);
    component_button(parent_node, "-", subtractFromTeam2);
    parent_node.appendChild(document.createElement("p"));    
    
    component_color(prefix,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(prefix,"Competition",parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(`${prefix}-t1`,"Team 1",parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_color(`${prefix}-t1`,parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_text(`${prefix}-t2`,"Team 2",parent_node);
    parent_node.appendChild(document.createElement("p"));
    component_color(`${prefix}-t2`,parent_node);
}

function alterScore(team,score){
    const el = document.getElementById(`score-c${team}-text-input`);
    el.value = parseInt(el.value) + score;
    send_to_rgb_matrix(generate_url({"name":"Score", "mode":"score", "team":`team${team}`,"update":score}));
}

function addToTeam1(){alterScore('1',1);}
function addToTeam2(){alterScore('2',1);}
function subtractFromTeam1(){alterScore('1',-1);}
function subtractFromTeam2(){alterScore('2',-1);}

function score_process(){
    const colour = document.getElementById('score-color-select');
    let competition = document.getElementById('score-text-input');
    let team1 = document.getElementById('score-t1-text-input');
    let team1_color = document.getElementById('score-t1-color-select');
    let team1_score = document.getElementById('score-c1-text-input');
    let team2 = document.getElementById('score-t2-text-input');
    let team2_color = document.getElementById('score-t2-color-select');
    let team2_score = document.getElementById('score-c2-text-input');
    
    competition.value = competition.value.trim();
    team1.value = team1.value.trim();
    team2.value = team2.value.trim();
    
    return {"name":"Score", "mins":0, "mode":"load", "color":colour.value, "competition":competition.value, "team1":team1.value, "team1_color":team1_color.value,"team1_score":team1_score.value, "team2":team2.value, "team2_color":team2_color.value,"team2_score":team2_score.value}
}