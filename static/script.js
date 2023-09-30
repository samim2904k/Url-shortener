function time_update(event){
    event.preventDefault();
    var long_url = document.getElementById("long_url").value;
    if(long_url==""){
        alert("Please Enter the valid site..");
        return;
    }
    var time_stamp = new Date().toString();
    fetch("/time_update",{  
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({time_stamp})
    });

    document.getElementById("myForm").submit();

}
