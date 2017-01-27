let fs = require('fs')
let pd = require('pretty-data').pd
let Entities = require('html-entities').XmlEntities;
var xml = require('xml2js').parseString;

let html = new Entities();

fs.readFile('data/raw.html', "utf-8", (err, data) => {
  if (err) throw err

  let lexicon = split_lexicon(data)

  lexicon.forEach((data, index) => {
    let out;
    switch (index) {
      case 0:
        break;
      case 1:
        out = do_title(data)
        write_section(data, "00-title.html")
        break;
      case 2:
        out= do_preface(data)
        write_section(data, "01-preface.html")
        break;
      case 3:
        out = do_abbr(data)
        write_section(data, "02-abbr.html")
        break;
      case 4:
        out = do_lex(data, "hebrew")
        break;
      case 5:
        out = do_lex(data, "aramaic")
        break;
      case 6:
        out = do_addenda(data)
        write_section(data, "05-addenda.html")
        break;
      default:
        console.log("Too many sections!")
        break;
    }
  });

});


function split_lexicon(data){
  data = data
    .split("<h1>")
  return data.map( section => {
    section = section.split("</h1>")
    return {
      title: section[0],
      content: section[1]
    }
  })

}

function write_section(obj, path){
  fs.writeFile('data/lexicon/'+ path, obj.content , err => {
    if (err) throw err;
  })
}

function prettify(obj){
  obj.content = pd.xml(obj.content)

  return obj
}

function do_title(title){
  title = format_h1(title)
  title.content = title.content
    .replace(/<p class="center">(.*)<\/p>/g, "$1")

  return prettify(title)

}
function do_preface(preface){
  preface = format_h1(preface)
  preface.content = preface.content
    .replace(/<p class="p">(.*)<\/p>/g, "<p>$1</p>")

  return prettify(preface)
}
function do_abbr(abbr){
  abbr = format_h1(abbr)
  abbr.content = abbr.content
    .replace(/<li style="list-style-type:none">(.*)<\/li>/g, "<li>$1</li>")
    .replace(/<p class="p">(.*)<\/p>/g, "<p>$1</p>")
  return prettify(abbr)
}
function do_lex(lex, lang){
  lex.content = lex.content
    .split(/<h2>/)

    note = lex.content.shift().trim()
    if (note.trim() !== ""){
      fs.writeFile('data/lexicon/' + lang + '/00-note.html', note , err => {
        if (err) throw err;
      })
    }

  lex.content = lex.content
    .map( (letter, index) => {
      letter = letter.split("</h2>")

      let title = letter[0].replace(/<span class="Bwhebb">(.*?)<\/span>/, "$1")
      if (index === 17){ title = "c" }
      return {
        title: html.decode(title),
        content: letter[1]
      }
    })
    .map( letter => {
      return do_letter_section(letter)
    })
    .forEach( (letter, index) => {
      fs.mkdir('data/lexicon/' + lang + '/' + index + "-" + letter.title, err => {
        if (err) throw err
      })
    })
}
function do_addenda(entries){ return do_letter_section(entries) }
function do_letter_section(lex){
  lex.content = lex.content
    .replace(/<!--(.*?)-->/g, "$1")
    .replace(/<p class="p">(.*)<\/p>/g, "$1")
    .split(/<ENTRY>/i)
    .filter( entry => {
      return entry.trim() !== ""
    })
    .map( data => {
      return pd.xml("<entry>" + data.trim() + "</entry>\n\n\n")
    })
    .map( data => {
      return html.decode(data)
    })
    .join("")
  return lex
}

function format_h1(section){
  section.content = "<h1>" + section.title + "</h1>\n" + section.content
  return section
}
