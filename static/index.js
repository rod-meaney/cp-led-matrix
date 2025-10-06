function fetchData(){
    fetch('./getdata')
    //fetch('http://rgb-matrix.local:5000/getdata')
    //fetch('http://192.168.0.122:5000/getdata')
    .then(response => {
        return response.json();
    })
    .then(data => {
        fetched_data = data;
    })
}

function load_any(any){
    current_select = any; //global
    let parent_node = document.getElementById('rgb-type');
    parent_node.innerHTML = "";
    document.getElementById('copy-url').innerHTML="";
    if (current_select!=''){
        parent_node.innerHTML = "";
        window[any+"_load"](parent_node); //Loads dynamic html

        //Create standard submit button
        let submit = document.createElement('button');
        submit.textContent = 'Request';
        submit.addEventListener('click', function() {
            window["send_any"](any);
        });
        parent_node.appendChild(document.createElement("p"));
        parent_node.appendChild(submit);
    }
}
function send_any(any){
    document.getElementById("sysmsg").innerHTML='';
    try {
        let jsonobj = window[any+"_process"]();
        let url = generate_url(jsonobj);
        send_to_rgb_matrix(url);
    } catch(err) {
        writemsg(err,false);
    }
}

function generate_url(jsonobj){
    const jsonString = JSON.stringify(jsonobj);
    const encodedJsonString = encodeURIComponent(jsonString);
    let url = "./loadjson?json=" + encodedJsonString;        

    //put the url in a box, select it so ut can be pasted
    document.getElementById('copy-url').innerHTML="";
    let copy = document.getElementById('copy-url');
    component_heading(copy,"h4","Url to copy");
    const copyurl = document.createElement("textarea");
    copyurl.rows = 5;
    copyurl.cols = 35;
    copyurl.id = 'copyurl';
    copyurl.value = url.replace('./', location.href);
    copy.appendChild(copyurl);
    const myInput = document.getElementById('copyurl');
    myInput.addEventListener('click', () => {
        myInput.select();
    });
    return url;
}

function send_to_rgb_matrix(url){
    //fetch('./loadmsg?{0}'.replace('{0}', params)) //soon
    fetch(url)
    .then(response => {
        if (!response.ok) {
            writemsg(`HTTP error! status: ${response.status}`, false);
        } else {
            writemsg('Request processed successfully');
        }
    });
}

function writemsg(msg,good=true){
    if (good===true){
        document.getElementById("sysmsg").innerHTML='<p>Message: {0}'.replace('{0}',msg);
        setTimeout(function() {
            document.getElementById("sysmsg").innerHTML='';
        }, 5000);    
    } else {
        console.log(msg);
        document.getElementById("sysmsg").innerHTML='<p style="font-weight: bold; color: red;">Error: {0}</p>'.replace('{0}',msg);
    }
}