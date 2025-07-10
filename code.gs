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
    const func = new Function(script);
    const result = func();
    return result || "✅ Script executed successfully.";
  } catch (error) {
    return "❌ Error: " + error.message;
  }
}


