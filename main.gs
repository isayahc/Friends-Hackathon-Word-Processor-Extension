function onOpen() {
  ScriptApp.newTrigger('main')
      .timeBased()
      .everyMinutes(1)
      .create();
}

const C = '\\[cit\\]';
const CHARS_BEFORE = 100;
const URL = 'https://bd6a-216-158-153-15.ngrok-free.app/query';
const NO_CONTEXT_CITATION = 'NO_CITATION_FOUND';

function main() {
  // Get the number for the citation
  let cit_number = getCitationsLength() + 1;

  // Replace each of the citations
  while (insertCitation(cit_number++)) {}
}

function getCitationsLength() {
  var body = DocumentApp.getActiveDocument().getBody();
  
  // Regular expression to match numbers inside square brackets
  var regex = /\[(\d+)\]/g;
  
  var text = body.getText();
  
  var numbers = [];
  var match;
  
  // Loop through matches and extract numbers
  while ((match = regex.exec(text)) !== null) {
    numbers.push(parseInt(match[1])); // Convert matched string to integer and push to array
  }
  
  // Find the highest number
  var highestNumber = numbers.length > 0 ? Math.max(...numbers) : 0;
  
  return highestNumber;
}

function insertCitation (cit_number) {
  var body = DocumentApp.getActiveDocument().getBody();

  let found = body.findText(C);
  if (found) {
    // Find the citation and remove it
    let start = found.getStartOffset();
    let end = found.getEndOffsetInclusive();
    let text = found.getElement().asText();
    text.deleteText(start, end);

    // Get the citation context
    let everythingBefore = body.getText().substring(0, start - 1);
    let context = everythingBefore.substring(everythingBefore.length - CHARS_BEFORE);
    let citation = get_citation(context);

    // If the context is null, it should 
    if (citation === null) {
      let replacement = '[' + NO_CONTEXT_CITATION + ']';
      text.insertText(start, replacement);

      // Don't add the full citation at the end
    }
    else {
      let replacement = '[' + cit_number + ']';
      text.insertText(start, replacement);

      // Add the full citation at the end
      const full_citation = cit_number + ". " + citation;
      body.appendParagraph(full_citation);
    }
  }

  return found;
}

function get_citation(context) {
  const data = {
    'query_string': context
  };
  const options = {
    'method' : 'post',
    'contentType': 'application/json',
    'payload' : JSON.stringify(data)
  };

  const res = UrlFetchApp.fetch(URL, options);
  const res_content = JSON.parse(res);

  // Return the citation if a good one exists, otherwise null
  if (res_content.is_fact_true) {
    return res_content.query_string;
  }
  else {
    return null;
  }
}
