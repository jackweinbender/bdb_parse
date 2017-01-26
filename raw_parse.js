let fs = require('fs')

fs.readFile('data/raw.html', "utf-8", (err, data) => {
  if (err) throw err;

  let lexicon = split_lexicon(data)

  for (var i = 0; i < lexicon.length; i++) {
    fs.writeFile('data/lexicon/' + i + " - " + lexicon[i].title + ".html", lexicon[i].content , err => {
      if (err) throw err;
    })
  }


});


function split_lexicon(data){
  // Splits raw.html into H1 sections
  data = data
    .split("<h1>")
    .map( section => {
      section = section.split("</h1>")
      return {
        title: section[0],
        content: section[1]
      }
    })
  data.shift()

  return data
}

function write_section(obj){

}
