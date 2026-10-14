-- {{< subscribe >}} shortcode: inserts the Buttondown sign-up form from
-- _subscribe-form.html (used on about.qmd and subscribe.qmd).

return {
  ["subscribe"] = function()
    local f = io.open(pandoc.path.join({quarto.project.directory, "_subscribe-form.html"}), "r")
    if not f then return pandoc.Null() end
    local form = f:read("a")
    f:close()
    return pandoc.RawBlock("html", form)
  end,
}
