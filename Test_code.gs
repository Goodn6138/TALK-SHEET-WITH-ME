function onOpen() {
  SpreadsheetApp.getUi().createMenu("SHEET TALK 😊")
    .addItem("Open Assistant", "openSheetTalk")
    .addToUi();
}

function openSheetTalk() {
  const html = HtmlService.createHtmlOutputFromFile("SheetTalk")
    .setWidth(400)
    .setHeight(300);
  SpreadsheetApp.getUi().showModalDialog(html, "SHEET TALK 😊");
}

function executeDynamicScript(script) {
  try {
    const result = eval(script);
    return result || "✅ Script executed successfully.";
  } catch (error) {
    return "❌ Error: " + error.message;
  }
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const script = data.command;

    const result = executeDynamicScript(script);
    
    return ContentService.createTextOutput(JSON.stringify({ result }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
