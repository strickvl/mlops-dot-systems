-- Adds a "Related posts" list to the end of each post listed in _related.json
-- (written by scripts/build_related.py as a pre-render step). A small script
-- moves the list into the right sidebar, under the table of contents, whenever
-- Quarto shows that sidebar (wide screens); on phones it stays at the bottom.
-- Quarto reads `margin-footer` before filters run, so it can't be used here.

local function esc(s)
  return (tostring(s):gsub("[&<>\"]", {["&"]="&amp;", ["<"]="&lt;", [">"]="&gt;", ['"']="&quot;"}))
end

local function load_related()
  local f = io.open(pandoc.path.join({quarto.project.directory, "_related.json"}), "r")
  if not f then return nil end
  local related = pandoc.json.decode(f:read("a"), false)
  f:close()
  return related
end

local MOVE_SCRIPT = [[<script>
(() => {
  const list = document.getElementById("related-posts");
  const sidebar = document.getElementById("quarto-margin-sidebar");
  const home = document.getElementById("related-posts-home");
  if (!list || !sidebar || !home) return;
  const place = () => {
    const sidebarShown = getComputedStyle(sidebar).display !== "none" && sidebar.offsetWidth > 0;
    (sidebarShown ? sidebar : home).appendChild(list);
    list.classList.toggle("in-sidebar", sidebarShown);
  };
  place();
  addEventListener("resize", place);
})();
</script>]]

function Pandoc(doc)
  if not quarto.doc.is_format("html") then return doc end
  local related = load_related()
  if not related then return doc end

  local rel = quarto.doc.input_file:sub(#quarto.project.directory + 2)
  local posts = related[rel]
  if not posts or #posts == 0 then return doc end

  local items = {}
  for _, p in ipairs(posts) do
    items[#items + 1] = string.format('<li><a href="%s">%s</a><span>%s · %s</span></li>',
      p.url, esc(p.title), p.section, p.date:sub(1, 4))
  end
  doc.blocks:insert(pandoc.RawBlock("html", string.format(
    '<div id="related-posts-home"><nav id="related-posts" aria-label="Related posts"><h2>Related posts</h2><ul>%s</ul></nav></div>%s',
    table.concat(items), MOVE_SCRIPT)))
  return doc
end
