const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');


signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});


signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});


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
    evt.currentTarget.className += " active";

    container.classList.remove("right-panel-active");
  }



// document.addEventListener("DOMContentLoaded", function () {
//     const navTabs = document.querySelectorAll(".nav-tab");

//     navTabs.forEach((tab) => {
//         tab.addEventListener("click", (event) => {
//             event.preventDefault();
//             const target = event.target.getAttribute("data-target");
//             const container = document.getElementById("container");

//             navTabs.forEach((t) => {
//                 t.classList.remove("active");
//             });

//             event.target.classList.add("active");

//             container.className = `container ${target}`;
//         });
//     });
// });

// document.addEventListener("DOMContentLoaded", function () {
//     const navTabs = document.querySelectorAll(".nav-tab");

//     navTabs.forEach((tab) => {
//         tab.addEventListener("click", (event) => {
//             event.preventDefault();
//             const target = event.target.getAttribute("data-target");
//             const container = document.getElementById("container");
//             const userHistoryContainer = document.getElementById("user-history-container");

//             navTabs.forEach((t) => {
//                 t.classList.remove("active");
//             });

//             event.target.classList.add("active");

//             if (target === "user-history-container") {
//                 userHistoryContainer.style.display = "block";
//             } else {
//                 userHistoryContainer.style.display = "none";
//             }

//             container.className = `container ${target}`;
//         });
//     });
// });

// $('#profile-tabs a').on('click', function (e) {
//     e.preventDefault()
//     $(this).tab('show')
//   })