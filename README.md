# [CI].ai
A word-processor extension which automatically replaces [cit] with the relevant citations for the material that the user is writing about.

Helps users to automatically generate citation for the papers or presentations they are creating, instead of having to search the web for justifying evidence.

## Example
    Magnus Carlsen won the 2018 FIDE World Chess Championship[cit]. 

As soon as the user finishes writing `[cit]`, the extension gets an appropriate source for the relevant content through an LLM call, formats the citation and updates the inline text appropriately. 

Concretely, this looks like `[cit]` becoming `[1]` (Or appropriate number if more citations already exist) and the citation text being added bottom of the document:

    1. Chess.com. (2018, November 28). Carlsen Wins 2018 World Chess Championship in Playoff. Chess.com. Retrieved from https://www.chess.com/news/view/carlsen-wins-2018-world-chess-championship-in-playoff

## How to demo
1. Open up a new google document:
https://docs.google.com/

2. Create a new document.

3. Go to **Extensions** then **Apps Script**.

4. Post in the supplied code (client.gs).

5. Hit **Run**.

6. The extension will scan your code every minute, and for each occurence of `[cit]` it will query the server. If a valid source is found, it will be appropriately referenced at the end of the document.

## Design choices
These are the tech that we chose to use for the project. Future development of this project would expand the selection of supported word-processing applications, available AI models, and citation formats.

Word processing application: Google Doc

LLM : Mixtral AI

Citation format : APA

Server : ngrok

## Edge-cases
Currently, if no relevant citation can be found, for example when the stated information isn't real, `[cit]` will be replaced with a `[NO_CITATION_FOUND]`. Alternatively we could pop-up a message alerting the user, or other behavior based on the desired user-experience.

## Future Improvement
Better error handling between client and server.

Improve the prompt and use of LLM.

Support more word-processors.
