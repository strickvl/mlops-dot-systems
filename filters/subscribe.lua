-- Adds the Buttondown sign-up form (_subscribe-form.html) to the end of every
-- post in posts/, personal/ and til/.

local function read_form()
  local f = io.open(pandoc.path.join({quarto.project.directory, "_subscribe-form.html"}), "r")
  if not f then return nil end
  local form = f:read("a")
  f:close()
  return form
end

function Pandoc(doc)
  if not quarto.doc.is_format("html") then return doc end
  local rel = quarto.doc.input_file:sub(#quarto.project.directory + 2)
  local dir = rel:match("^([^/]+)/[^/]+$")
  if dir ~= "posts" and dir ~= "personal" and dir ~= "til" then return doc end
  local form = read_form()
  if form then doc.blocks:insert(pandoc.RawBlock("html", form)) end
  return doc
end
