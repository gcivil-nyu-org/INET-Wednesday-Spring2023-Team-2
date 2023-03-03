const body = document.querySelector('body'),
      sidebar = document.body.querySelector('nav'),
      toggle = document.body.querySelector(".toggle"),
      searchBtn = document.body.querySelector(".search-box"),
      modeSwitch = document.body.querySelector(".toggle-switch"),
      modeText = document.body.querySelector(".mode-text");



toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
})

searchBtn.addEventListener("click" , () =>{
    sidebar.classList.remove("close");
})

modeSwitch.addEventListener("click" , () =>{
    body.classList.toggle("dark");
    
    if(body.classList.contains("dark")){
        modeText.innerText = "Light mode";
    }else{
        modeText.innerText = "Dark mode";
        
    }
});