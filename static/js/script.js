async function sendRequest() {
  text = document.getElementById("req-text").value;
  const res = await fetch("/run?task=" + text, {
    method: "POST",
  });
  const json = await res.json();
  console.log(json);
}
function getFile() {
  file = document.getElementById("file-url").value;
  window.location.href = "/read?path=" + file;
}
