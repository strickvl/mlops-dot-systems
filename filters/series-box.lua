-- Adds a series box to the top and previous/next links to the bottom of any
-- post listed in _series.json (written by scripts/build_series.py, which runs
-- as a Quarto pre-render step).

local MONTHS = {"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"}

local function esc(s)
  return (tostring(s):gsub("[&<>\"]", {["&"]="&amp;", ["<"]="&lt;", [">"]="&gt;", ['"']="&quot;"}))
end

local function month(d)
  return MONTHS[tonumber(d:sub(6, 7))] .. " " .. d:sub(1, 4)
end

local function load_index()
  local f = io.open(pandoc.path.join({quarto.project.directory, "_series.json"}), "r")
  if not f then return nil end
  local index = pandoc.json.decode(f:read("a"), false)
  f:close()
  return index
end

local function parts_list(s, here)
  local items = {}
  for i, p in ipairs(s.posts) do
    local cls = (i == here) and ' class="series-here"' or ""
    items[#items + 1] = string.format('<li%s><a href="%s">%s</a> <span class="series-date">%s</span></li>',
      cls, p.url, esc(p.title), month(p.date))
  end
  return '<ol class="series-parts">' .. table.concat(items) .. "</ol>"
end

local function top_box(s, here)
  local ongoing = s.ongoing and ' <span class="series-ongoing">ongoing</span>' or ""
  return string.format([[<div class="series-box"><div class="series-box-head"><span class="series-part">Part %d of %d</span> <a href="/series.html#%s">%s</a>%s</div><details><summary>All parts</summary>%s</details></div>]],
    here, #s.posts, s.id, esc(s.title), ongoing, parts_list(s, here))
end

local function nav_link(p, label, cls)
  return string.format('<a class="%s" href="%s"><small>%s</small>%s</a>', cls, p.url, label, esc(p.title))
end

local function bottom_nav(s, here)
  local prev = s.posts[here - 1] and nav_link(s.posts[here - 1], "← Part " .. (here - 1), "series-prev") or "<span></span>"
  local nxt = s.posts[here + 1] and nav_link(s.posts[here + 1], "Part " .. (here + 1) .. " →", "series-next") or ""
  return string.format([[<nav class="series-nav"><div class="series-nav-label">Part %d of %d in <a href="/series.html#%s">%s</a></div><div class="series-nav-links">%s%s</div></nav>]],
    here, #s.posts, s.id, esc(s.title), prev, nxt)
end

function Pandoc(doc)
  if not quarto.doc.is_format("html") then return doc end
  local index = load_index()
  if not index then return doc end

  local input = quarto.doc.input_file
  local rel = input:sub(#quarto.project.directory + 2)
  local memberships = index.posts[rel]
  if not memberships then return doc end

  local by_id = {}
  for _, s in ipairs(index.series) do by_id[s.id] = s end

  local top, bottom = {}, {}
  for _, m in ipairs(memberships) do
    local s, here = by_id[m.series], math.tointeger(m.index) + 1
    top[#top + 1] = top_box(s, here)
    bottom[#bottom + 1] = bottom_nav(s, here)
  end

  table.insert(doc.blocks, 1, pandoc.RawBlock("html", table.concat(top)))
  doc.blocks:insert(pandoc.RawBlock("html", '<div class="series-footer">' .. table.concat(bottom) .. "</div>"))
  return doc
end
