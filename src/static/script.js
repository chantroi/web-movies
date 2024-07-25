import { Deta } from "https://cdn.deta.space/js/deta@latest/deta.mjs";

document.addEventListener("DOMContentLoaded", function () {
  const deta = Deta(detaKey);
  const drive = deta.Drive(driveName);
  const fileLinks = document.querySelectorAll(".file-link");
  const videoPlayer = document.getElementById("videoPlayer");
  let videoCache = {};
  let currentVideo;
  let preVideo;
  let nextVideo;

  async function fetchVideo(filename) {
    if (!videoCache[filename]) {
      try {
        const response = await drive.get(filename);
        const blob = new Blob([response]);
        videoCache[filename] = URL.createObjectURL(blob);
      } catch (error) {
        console.error("Error fetching video:", filename, error);
      }
    }
    return videoCache[filename];
  }

  async function initVideo(filename) {
    try {
      const videoUrl = await fetchVideo(filename);
      videoPlayer.src = videoUrl;
      await videoPlayer.play();
      if (videoPlayer.requestFullscreen) {
        await videoPlayer.requestFullscreen();
      } else if (videoPlayer.mozRequestFullScreen) {
        await videoPlayer.mozRequestFullScreen();
      } else if (videoPlayer.webkitRequestFullscreen) {
        await videoPlayer.webkitRequestFullscreen();
      } else if (videoPlayer.msRequestFullscreen) {
        await videoPlayer.msRequestFullscreen();
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function renewVideo(filename) {
    const response = await fetch(`/${driveName}/${filename}?renew=true`);
    const data = await response.json();
    currentVideo = filename;
    nextVideo = data.next;
    preVideo = data.pre;
    if (nextVideo) fetchVideo(nextVideo);
    if (preVideo) fetchVideo(preVideo);
  }

  async function playNextVideo() {
    if (nextVideo) {
      await initVideo(nextVideo);
      renewVideo(nextVideo);
    }
  }

  async function playPreviousVideo() {
    if (preVideo) {
      await initVideo(preVideo);
      renewVideo(preVideo);
    }
  }

  function handleFullscreenChange() {
    if (
      !document.fullscreenElement &&
      !document.webkitIsFullScreen &&
      !document.mozFullScreen &&
      !document.msFullscreenElement
    ) {
      videoPlayer.pause();
      videoPlayer.currentTime = 0;
      videoPlayer.src = "";
    }
  }

  fileLinks.forEach((link) => {
    link.addEventListener("click", async function (e) {
      e.preventDefault();
      const filename = this.getAttribute("data-file");
      currentVideo = filename;
      await initVideo(filename);
      renewVideo(filename);
    });
  });

  document.addEventListener("fullscreenchange", handleFullscreenChange);
  document.addEventListener("webkitfullscreenchange", handleFullscreenChange);
  document.addEventListener("mozfullscreenchange", handleFullscreenChange);
  document.addEventListener("MSFullscreenChange", handleFullscreenChange);

  videoPlayer.addEventListener("ended", playNextVideo);

  let touchStart;
  document.addEventListener(
    "touchstart",
    (e) => {
      touchStart = e.changedTouches[0].screenX;
    },
    { passive: true }
  );

  document.addEventListener(
    "touchend",
    async (e) => {
      const touchEnd = e.changedTouches[0].screenX;
      const touchDiff = touchEnd - touchStart; // Đã sửa đổi ở đây

      if (Math.abs(touchDiff) > 50) {
        // Ngưỡng để xác định hành động vuốt
        if (touchDiff > 0) {
          // Vuốt sang phải (trái sang phải)
          await playNextVideo();
        } else {
          // Vuốt sang trái (phải sang trái)
          await playPreviousVideo();
        }
      }
    },
    { passive: true }
  );

  document.addEventListener("keydown", async (e) => {
    if (e.key === "ArrowLeft") {
      await playPreviousVideo();
    } else if (e.key === "ArrowRight") {
      await playNextVideo();
    }
  });
});
