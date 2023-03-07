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