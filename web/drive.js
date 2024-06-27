import { Deta } from "https://cdn.deta.space/js/deta@latest/deta.mjs";

const deta = Deta(process.env.DETA_KEY);
const drive = deta.Base("files");

async function listFiles() {
  const player = document.createElement("iframe");
  player.setAttribute("id", "player-div");
  player.setAttribute("width", "100%");
  player.setAttribute("frameborder", "0");
  player.setAttribute("allowfullscreen", "");
  document.getElementById("root").appendChild(player);
  const result = await drive.list();
  const files = result.names;
  const ulTag = document.createElement("ul");
  ulTag.setAttribute("class", "collection");
  for (file of files) {
    const liTag = document.createElement("li");
    liTag.setAttribute("class", "collection-item");
    const aTag = document.createElement("a");
    aTag.setAttribute("href", file);
    aTag.setAttribute("target", "player-div");
    aTag.innerText = file;
    liTag.appendChild(aTag);
    ulTag.appendChild(liTag);
  }
  document.getElementById("root").appendChild(ulTag);
}

listFiles();
