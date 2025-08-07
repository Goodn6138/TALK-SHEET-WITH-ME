function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("AI Assistant")
    .addItem("Ping Server", "openPingDialog")
    .addToUi();
}

function openPingDialog() {
  const html = HtmlService.createHtmlOutputFromFile("UI")
    .setWidth(400)
    .setHeight(200);
  SpreadsheetApp.getUi().showModalDialog(html, "Ping Server");
}

function pingBackend() {
  const url = "https://ai-assistant-ping.onrender.com/ping";  // replace with your real URL
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ message: "hello from google script" }),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  return response.getContentText();
}

