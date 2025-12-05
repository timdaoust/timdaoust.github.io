document.addEventListener("DOMContentLoaded", () => {
  const videoLayer = document.getElementById("video-layer");
  const contentLayer = document.getElementById("content-layer");
  const video = document.getElementById("introVideo");
  const skipBtn = document.getElementById("skip-btn");

  function showContent() {
    // Fade out video, fade in content
    videoLayer.classList.add("fade-out");
    contentLayer.hidden = false;
    contentLayer.classList.add("fade-in");

    // After transition, fully hide video layer so it doesn't eat scroll events
    setTimeout(() => {
      videoLayer.style.display = "none";
    }, 950);
  }

  if (video) {
    video.addEventListener("ended", () => {
      showContent();
    });
  }

  if (skipBtn) {
    skipBtn.addEventListener("click", (event) => {
      event.preventDefault();
      if (video && !video.paused) {
        video.pause();
      }
      showContent();
    });
  }
});
