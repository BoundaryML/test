
class Output {
  summary string
}

function ExtractFromImage(img: image) -> Output {
  client FastOpenAI
  prompt #"
    Extract from this image
    {{ ctx.output_format }}

    {{ _.role("user") }}
    {{ img }}
  "#
}

test TestOne {
  functions [ExtractFromImage]
  args {
    img {
      file "./invoice.png"
    }
  }
}
