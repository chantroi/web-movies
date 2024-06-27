import { Deta } from "https://cdn.deta.space/js/deta@latest/deta.mjs";

const deta = Deta(process.env.DETA_KEY);
const drive = deta.Base("files");

async function listFiles() {
  const result = await drive.list();
  const files = result.names;
  const ulTag = document.createElement("ul");
  ulTag.setAttribute("class", "collection");
  files.forEach((file) => {
    const liTag = document.createElement("li");
    liTag.setAttribute("class", "collection-item");
    const aTag = document.createElement("a");
    aTag.setAttribute("onclick", `playVideo("${file}")`);
    aTag.setAttribute("target", "player-div");
    aTag.innerText = file;
    liTag.appendChild(aTag);
    ulTag.appendChild(liTag);
  });
  document.getElementById("root").appendChild(ulTag);
}

async function playVideo(file) {
  const player = document.createElement("video");
  player.setAttribute("id", "player-div");
  document.getElementById("header").appendChild(player);
  const result = await drive.get(file);
  const blob = new Blob([result]);
  const url = URL.createObjectURL(blob);
  document.getElementById("player-div").src = url;
}

listFiles();
