const sampleNode = document.getElementById("sample-data");
if (sampleNode) {
  const samples = JSON.parse(sampleNode.textContent);
  document.querySelectorAll("[data-sample]").forEach((button) => {
    button.addEventListener("click", () => {
      const sample = samples[button.dataset.sample];
      if (!sample) return;
      const channel = document.querySelector(`input[name="channel"][value="${sample.channel}"]`);
      if (channel) channel.checked = true;
      const text = document.getElementById("text-input");
      const url = document.getElementById("url-input");
      if (text) text.value = sample.text;
      if (url) url.value = sample.url;
    });
  });
}
