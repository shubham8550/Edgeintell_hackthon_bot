function doGet(e){

  var op = e.parameter.action;

  var ss=SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/edit?usp=sharing");
  var sheet = ss.getSheetByName("Sheet2");


  if(op=="insert")
    return insert_value(e,sheet);

  //Make sure you are sending proper parameters
  if(op=="read")
    return read_value(e,ss);




}

//Recieve parameter and pass it to function to handle




function insert_value(request,sheet){


   var name = request.parameter.name;
   var company =request.parameter.company;
  var website = request.parameter.website;
  var linkedin = request.parameter.linkedin;

  var flag=1;
  var lr= sheet.getLastRow();
  for(var i=1;i<=lr;i++){
    var id1 = sheet.getRange(i, 4).getValue();
    if(id1==name){
      flag=0;
  var result="Company already exist..";
    } }
  //add new row with recieved parameter from client
  if(flag==1){
  var d = new Date();
    var currentTime = d.toLocaleString();
  var rowData = sheet.appendRow([name,company,website,linkedin]);
  var result="Insertion successful";
  }
     result = JSON.stringify({
    "result": result
  });

  return ContentService
  .createTextOutput(request.parameter.callback + "(" + result + ")")
  .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }





function read_value(request,ss){


  var output  = ContentService.createTextOutput(),
      data    = {};

      var sheet="Sheet2";

  data.records = readData_(ss, sheet);

  var callback = request.parameters.callback;

  if (callback === undefined) {
    output.setContent(JSON.stringify(data));
  } else {
    output.setContent(callback + "(" + JSON.stringify(data) + ")");
  }
  output.setMimeType(ContentService.MimeType.JAVASCRIPT);

  return output;
}


function readData_(ss, sheetname, properties) {

  if (typeof properties == "undefined") {
    properties = getHeaderRow_(ss, sheetname);
    properties = properties.map(function(p) { return p.replace(/\s+/g, '_'); });
  }

  var rows = getDataRows_(ss, sheetname),
      data = [];

  for (var r = 0, l = rows.length; r < l; r++) {
    var row     = rows[r],
        record  = {};

    for (var p in properties) {
      record[properties[p]] = row[p];
    }

    data.push(record);

  }
  return data;
}



function getDataRows_(ss, sheetname) {
  var sh = ss.getSheetByName(sheetname);

  return sh.getRange(2, 1, sh.getLastRow() - 1, sh.getLastColumn()).getValues();
}


function getHeaderRow_(ss, sheetname) {
  var sh = ss.getSheetByName(sheetname);

  return sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
}

