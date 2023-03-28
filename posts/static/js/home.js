let currentPoll = 1;
  const maxPoll = 2;

  function showNextPoll() {
    currentPoll++;
    if (currentPoll > maxPoll) {
      currentPoll = 1;
    }
    showCurrentPoll();
  }

  function showPrevPoll() {
    currentPoll--;
    if (currentPoll < 1) {
      currentPoll = maxPoll;
    }
    showCurrentPoll();
  }


  function showCurrentPoll() {
    const pollContainers = document.getElementsByClassName('container');
    for (let i = 0; i < pollContainers.length; i++) {
      pollContainers[i].style.display = 'none';
    }
    const currentPollContainer = document.getElementById(`poll${currentPoll}`);
    currentPollContainer.style.display = 'block';
    pollContainers.classList.add("right-panel-active");
  }


  function chBackcolor(id) {
    if(document.getElementById("yolo1")){
      document.getElementById("yolo1").style.backgroundColor = "#f2f2f2";
    }
    if(document.getElementById("yolo2")){
      document.getElementById("yolo2").style.backgroundColor = "#f2f2f2";
    }
    if(document.getElementById("yolo3")){
      document.getElementById("yolo3").style.backgroundColor = "#f2f2f2";
    }
    if(document.getElementById("yolo4")){
      document.getElementById("yolo4").style.backgroundColor = "#f2f2f2";
    }
    document.getElementById(id).style.backgroundColor = "#555";
 }

 function registerCategoryTabs() {
  document.getElementById("nav-sports-tab").addEventListener("click", function () {
    const url = this.getAttribute("data-url");
    getCategoryBasedPost(url);
  });

  document.getElementById("nav-entertainment-tab").addEventListener("click", function () {
    const url = this.getAttribute("data-url");
    getCategoryBasedPost(url);
  });

  document.getElementById("nav-misc-tab").addEventListener("click", function () {
    const url = this.getAttribute("data-url");
    getCategoryBasedPost(url);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  registerCategoryTabs();
});

// function getCategoryBasedPost(url) {
//   fetch(url)
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.status === "success") {
//         showCategoryBasedPost(data.post_id);
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching category-based post:", error);
//     });
// }

function getCategoryBasedPost(url) {
  fetch(url)
    .then((response) => response.text())
    .then((html) => {
      document.getElementById("poll-container").innerHTML = html;
      registerVoteButtons();
    })
    .catch((error) => {
      console.warn(error);
    });
}

function showCategoryBasedPost(post_id) {
  window.location.href = `{% url 'posts:post_generation_page' 0 %}`.replace(/0$/, post_id);
}


 

// function getCategoryBasedPost(category) {
//   let url = "{% url 'posts:show_categorybased_post_api' 'dummy_category' %}".replace("dummy_category", category);
//   fetch(url)
//       .then((response) => response.text())
//       .then((data) => {
//           document.getElementById("postDispDiv").innerHTML = data;
//       });
// }





//  document.getElementById("poll-container").click();

// function openTab(evt, tabName) {
//     // Declare all variables
//     var i, tabcontent, tablinks;
  
//     // Get all elements with class="tabcontent" and hide them
//     tabcontent = document.getElementsByClassName("container");
//     for (i = 0; i < tabcontent.length; i++) {
//       tabcontent[i].style.display = "none";
//     }
  
//     // Get all elements with class="tablinks" and remove the class "active"
//     tablinks = document.getElementsByClassName("nav-tab");
//     for (i = 0; i < tablinks.length; i++) {
//       tablinks[i].className = tablinks[i].className.replace(" active", "");
//     }
  
//     // Show the current tab, and add an "active" class to the button that opened the tab
//     document.getElementById(tabName).style.display = "block";
//     evt.currentTarget.className += " active";


  //   if (tabName === "nav-profile") {
  //     document.getElementsByClassName("profile-info-container")[0].style.display = "flex";
  // } else {
  //     document.getElementsByClassName("profile-info-container")[0].style.display = "none";
  // }


  // }




  // function fetchCategoryBasedPoll(category) {
  //   const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  //   const pollContainer = document.getElementById("poll-container");

  //   fetch(`/posts/show_category_based_post/${category}/`, {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //       "X-CSRFToken": csrfToken
  //     }
  //   })
  //     .then(response => {
  //       if (response.ok) {
  //         return response.text();
  //       } else {
  //         throw new Error("Error fetching the poll data.");
  //       }
  //     })
  //     .then(data => {
  //       pollContainer.innerHTML = data;
  //     })
  //     .catch(error => {
  //       console.error("Error fetching the poll data:", error);
  //     });
  // }

  // document.addEventListener("DOMContentLoaded", function () {
  //   // Get all category tabs and add event listeners
  //   const categoryTabs = [
  //     "nav-all-tab",
  //     "nav-sports-tab",
  //     "nav-entertainment-tab",
  //     "nav-misc-tab"
  //   ];

  //   categoryTabs.forEach((tabId) => {
  //     const tab = document.getElementById(tabId);
  //     tab.addEventListener("click", function () {
  //       const category = tabId.replace("nav-", "").replace("-tab", "");
  //       fetchCategoryBasedPoll(category);
  //     });
  //   });

  //   // Fetch the initial poll
  //   getCurrPost();
  // });
