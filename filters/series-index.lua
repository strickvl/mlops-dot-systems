-- {{< series-index >}} shortcode: renders the timeline of all series on
-- series.qmd from _series.json (written by scripts/build_series.py).

local MONTHS = {"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"}

local function esc(s)
  return (tostring(s):gsub("[&<>\"]", {["&"]="&amp;", ["<"]="&lt;", [">"]="&gt;", ['"']="&quot;"}))
end

local function month(d)
  return MONTHS[tonumber(d:sub(6, 7))] .. " " .. d:sub(1, 4)
end

-- Position of a YYYY-MM-DD date as a fractional year, e.g. 2021-07-01 -> 2021.5
local function year_frac(d)
  return tonumber(d:sub(1, 4)) + (tonumber(d:sub(6, 7)) - 1) / 12
end

local function render(index)
  local today = os.date("%Y-%m-%d")
  local y0, y1 = math.huge, tonumber(today:sub(1, 4)) + 1
  local by_url, counts = {}, {all = 0}
  for _, s in ipairs(index.series) do
    y0 = math.min(y0, tonumber(s.start:sub(1, 4)))
    counts.all = counts.all + 1
    counts[s.section] = (counts[s.section] or 0) + 1
    for i, p in ipairs(s.posts) do
      by_url[p.url] = by_url[p.url] or {}
      table.insert(by_url[p.url], {s = s, i = i})
    end
  end
  local pct = function(d) return (year_frac(d) - y0) / (y1 - y0) * 100 end

  local out = {'<div class="series-filters" role="group" aria-label="Filter series">'}
  for _, f in ipairs({"all", "technical", "personal"}) do
    out[#out + 1] = string.format('<button type="button" data-filter="%s" aria-pressed="%s">%s <span>%d</span></button>',
      f, tostring(f == "all"), f:sub(1, 1):upper() .. f:sub(2), counts[f] or 0)
  end
  out[#out + 1] = '</div><div class="series-axis" aria-hidden="true">'
  for y = y0, y1 - 1, 2 do
    out[#out + 1] = string.format('<span style="left:%.2f%%">%d</span>', pct(y .. "-01-01"), y)
  end
  out[#out + 1] = '</div><div class="series-timeline">'

  for _, s in ipairs(index.series) do
    local a, b = pct(s.start), pct(s.ongoing and today or s["end"])
    local span = month(s.start) .. " – " .. (s.ongoing and "now" or month(s["end"]))
    local ongoing = s.ongoing and '<span class="series-ongoing">ongoing</span>' or ""
    local items = {}
    for i, p in ipairs(s.posts) do
      local also = {}
      for _, o in ipairs(by_url[p.url]) do
        if o.s.id ~= s.id then
          also[#also + 1] = string.format('part %d of <a href="#%s">%s</a>', o.i, o.s.id, esc(o.s.title))
        end
      end
      local also_html = #also > 0 and ('<span class="series-also">also ' .. table.concat(also, ", ") .. "</span>") or ""
      items[#items + 1] = string.format('<li><a href="%s">%s</a><span class="series-date">%s</span>%s</li>',
        p.url, esc(p.title), month(p.date), also_html)
    end
    out[#out + 1] = string.format([[<section class="series-entry" id="%s" data-section="%s">
<div class="series-track" aria-hidden="true"><i class="%s%s" style="left:%.2f%%;width:%.2f%%"></i></div>
<div class="series-meta"><span class="series-section %s">%s</span><span>%s · %d parts</span>%s</div>
<h2 class="anchored">%s</h2><p>%s</p><ol class="series-parts">%s</ol></section>]],
      s.id, s.section, s.section, s.ongoing and " ongoing" or "", a, math.max(b - a, 0.6),
      s.section, s.section, span, #s.posts, ongoing, esc(s.title), esc(s.description), table.concat(items))
  end
  out[#out + 1] = "</div>"
  return table.concat(out, "\n")
end

return {
  ["series-index"] = function()
    local f = io.open(pandoc.path.join({quarto.project.directory, "_series.json"}), "r")
    if not f then return pandoc.Para("Series index missing: run scripts/build_series.py.") end
    local index = pandoc.json.decode(f:read("a"), false)
    f:close()
    return pandoc.RawBlock("html", render(index))
  end,
}
