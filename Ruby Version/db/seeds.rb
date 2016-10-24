# ---------
#   Data
# ---------
authors = %w(Will David Jeff John Eric)

contents = [
  "Maybe our mistakes are what make our fate. Without them, what would shape our lives? Perhaps, if we never veered off course, we wouldn't fall in love or have babies or be who we are.",
  "Young people have an almost biological destiny to be hopeful.",
  "In the depth of winter, I finally learned that within me there lay an invincible summer.",
  "Now that I've relinquished my fantasies of all the people I wish I could be, and stopped feeling guilty about [them], I have more time for the things that I truly enjoy.",
  "The most wasted of all days is one without laughter.",
  "The best way to live is by not knowing what will happen to you at the end of the day.",
  "There is always a well-known solution to every human problem--neat, plausible, and wrong.",
  "There are no such things as applied sciences, only applications of science.",
  "Fidelity to commitment in the face of doubts and fears is a very spiritual thing.",
  "Think not those faithful who praise all thy words and actions; but those who kindly reprove thy faults.",
  "The best way to learn to be an honest, responsible adult is to live with adults who act honestly and responsibly.",
  "If at first you don't succeed, failure may be your style."
]

images = [
  "http://fillmurray.com/300/300",
  "http://placecage.com/200/200",
  "http://placecage.com/300/300"]

# ---------
#  Seeding
# ---------

Squawk.destroy_all

contents.each do |content|
  Squawk.create({
    author: authors.sample,
    content: content,
    image_url: images.sample
  })
end
