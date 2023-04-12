// const editButton = document.getElementById('editProfile');
// const backButton = document.getElementById('back');
// const container = document.getElementById('container');


// editButton.addEventListener('click', () => {
// 	container.classList.add("right-panel-active");
// });


// backButton.addEventListener('click', () => {
// 	container.classList.remove("right-panel-active");
// });


// document.getElementById("nav-profile").click();

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("nav-tab");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    // evt.currentTarget.className += " active";
    main_tablink = document.getElementById(tabName.toString() + "-tab");
    main_tablink.className += " active";


    if (tabName === "nav-profile") {
      document.getElementsByClassName("profile-info-container")[0].style.display = "flex";
  } else {
      document.getElementsByClassName("profile-info-container")[0].style.display = "none";
  }


  }



