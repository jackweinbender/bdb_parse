let fs = require('fs')
let pd = require('pretty-data').pd
let Entities = require('html-entities').XmlEntities;

let html = new Entities();

fs.readFile('raw.html', "utf-8", (err, data) => {
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
        write_section(out, "02-abbr.html")
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
  fs.writeFile('../lexicon/'+ path, obj.content , err => {
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
    .replace(/<span class="greek">(.*?)<\/span>/g, "<greek>$1</greek>")

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

  lex.content.unshift(note.trim())
  lex.content = lex.content.join("")
  lex.content = `<lexicon lang=${lang}>` + lex.content + `</lexicon>`

  switch (lang) {
    case "aramaic":
      file = "04-aramaic.html"
      break;
    default:
      file = "03-hebrew.html"
      break;
  }

  fs.writeFile("../lexicon/" + file, lex.content, err => {
    if (err) throw err;
  })
}
function do_addenda(entries){ return do_letter_section(entries) }
function do_letter_section(letter){
  letter.content = letter.content
    .replace(/<!--/g, "")
    .replace(/-->/g, "")
    .replace(/\n/g, "")
    .replace(/<p class="p">/g, "")
    .replace(/<\/p>/g, "")
    .replace(/<span class="Bwhebb">(.*?)<\/span>/g, "<hebrew>$1</hebrew>")
    .replace(/<span class="syriac">(.*?)<\/span>/g, "<syriac>$1</syriac>")
    .replace(/<span class="arabic">(.*?)<\/span>/g, "<arabic>$1</arabic>")
    .replace(/<span class="ethiopic">(.*?)<\/span>/g, "<ethiopic>$1</ethiopic>")
    .replace(/<span class="greek">(.*?)<\/span>/g, "<greek>$1</greek>")
    .replace(/<span class="samaritan">(.*?)<\/span>/g, "<samaritan>$1</samaritan>")
    .replace(/<span class="persian">(.*?)<\/span>/g, "<persian>$1</persian>")
    .replace(/<span style="color:blue">(\d+):<\/span>\s*/g, "$1" )
    .replace(/<(\/*)STRONGS>/g, "<$1strongs>" )
    .replace(/<(\/*)ENTRYNUM>/g, "<$1entrynum>" )
    .replace(/<(\/*)PAGE>/g, "<$1page>" )
    .split(/<entry>/i)
    .filter( entry => {
      return entry.trim() != ""
    })
    .map( data => {
      return html.decode(data)
    })
    .map( data => {
      return `<entry>${data}</entry>`
    })
    .join("")
  return `<letter letter=${letter.title}>` + letter.content + `</letter>`
}

function format_h1(section){
  section.content = "<h1>" + section.title + "</h1>\n" + section.content
  return section
}
