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
    const pollContainers = document.getElementsByClassName('poll-container');
    for (let i = 0; i < pollContainers.length; i++) {
      pollContainers[i].style.display = 'none';
    }
    const currentPollContainer = document.getElementById(`poll${currentPoll}`);
    currentPollContainer.style.display = 'block';
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
