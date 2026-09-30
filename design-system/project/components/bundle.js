/* @ds-bundle: {"format":4,"namespace":"Retro","components":[{"name":"RetroWindow"},{"name":"SystemSwitcher"},{"name":"PaletteGrid"}]} */
(function () {
  "use strict";
  var SYSTEMS = [{"num": 1, "id": "macsys7", "name": "Mac System 7", "era": "Desktop OS", "year": 1991, "tags": ["mac", "monochrome", "bevel", "classic"], "font": "\"Chicago\", \"Charcoal\", \"Geneva\", Tahoma, sans-serif", "featured": false}, {"num": 2, "id": "win95", "name": "Windows 95", "era": "Desktop OS", "year": 1995, "tags": ["windows", "bevel", "chrome", "classic"], "font": "\"MS Sans Serif\", \"Pixelated MS Sans Serif\", Tahoma, sans-serif", "featured": true}, {"num": 3, "id": "xpluna", "name": "Windows XP Luna", "era": "Desktop OS", "year": 2001, "tags": ["windows", "glossy", "blue", "luna"], "font": "\"Trebuchet MS\", \"Tahoma\", \"Franklin Gothic Medium\", sans-serif", "featured": false}, {"num": 4, "id": "aqua", "name": "Mac OS X Aqua", "era": "Desktop OS", "year": 2001, "tags": ["mac", "glossy", "gel", "aqua"], "font": "\"Lucida Grande\", \"Helvetica Neue\", sans-serif", "featured": false}, {"num": 5, "id": "amiga", "name": "Amiga Workbench", "era": "Desktop OS", "year": 1985, "tags": ["amiga", "retro", "orange", "blue"], "font": "\"Topaz\", \"Courier New\", \"Consolas\", monospace", "featured": false}, {"num": 6, "id": "nextstep", "name": "NeXTSTEP", "era": "Desktop OS", "year": 1989, "tags": ["next", "greyscale", "unix", "chiseled"], "font": "\"Helvetica Neue\", \"Helvetica\", \"Liberation Sans\", sans-serif", "featured": false}, {"num": 7, "id": "beos", "name": "BeOS", "era": "Desktop OS", "year": 1996, "tags": ["beos", "yellow", "tab", "media"], "font": "\"Swiss 721\", \"Helvetica\", \"Swis721 BT\", sans-serif", "featured": false}, {"num": 8, "id": "teletext", "name": "Teletext", "era": "Broadcast", "year": 1974, "tags": ["teletext", "blocky", "primary", "tv"], "font": "\"VT323\", \"Courier New\", \"Consolas\", monospace", "featured": false}, {"num": 9, "id": "crt", "name": "CRT Phosphor Terminal", "era": "Terminal", "year": 1980, "tags": ["terminal", "green", "scanline", "phosphor"], "font": "\"VT323\", \"IBM Plex Mono\", \"Courier New\", monospace", "featured": true}, {"num": 10, "id": "doscga", "name": "DOS CGA", "era": "Terminal", "year": 1981, "tags": ["dos", "cyan", "magenta", "4-color"], "font": "\"Perfect DOS VGA 437\", \"IBM Plex Mono\", \"Courier New\", monospace", "featured": false}, {"num": 11, "id": "arcade", "name": "8-Bit Arcade", "era": "Gaming", "year": 1983, "tags": ["arcade", "pixel", "neon", "8-bit"], "font": "\"Press Start 2P\", \"VT323\", monospace", "featured": true}, {"num": 12, "id": "aero", "name": "Frutiger Aero", "era": "Web/UI", "year": 2007, "tags": ["aero", "glossy", "nature", "glass"], "font": "\"Frutiger\", \"Segoe UI\", \"Myriad Pro\", \"Helvetica Neue\", sans-serif", "featured": false}, {"num": 13, "id": "winamp", "name": "Winamp Skin", "era": "App", "year": 1997, "tags": ["winamp", "media", "skin", "lcd"], "font": "\"Helvetica Neue\", Arial, sans-serif", "featured": false}, {"num": 14, "id": "geocities", "name": "GeoCities Web 1.0", "era": "Web", "year": 1996, "tags": ["web1.0", "kitsch", "gif", "tiled"], "font": "\"Comic Sans MS\", \"Times New Roman\", serif", "featured": false}, {"num": 15, "id": "cassette", "name": "Cassette Futurism", "era": "Sci-Fi", "year": 1979, "tags": ["scifi", "control-panel", "amber", "analog"], "font": "\"Orbitron\", \"Share Tech Mono\", \"Courier New\", monospace", "featured": false}, {"num": 16, "id": "vaporwave", "name": "Vaporwave", "era": "Aesthetic", "year": 2011, "tags": ["vaporwave", "pastel", "synth", "neon"], "font": "\"Times New Roman\", \"Hiragino Mincho Pro\", serif", "featured": true}, {"num": 17, "id": "memphis", "name": "Memphis", "era": "Design", "year": 1981, "tags": ["memphis", "postmodern", "primary", "squiggle"], "font": "\"Helvetica Neue\", Helvetica, Impact, sans-serif", "featured": false}, {"num": 18, "id": "ps1", "name": "PS1 Tech", "era": "Gaming", "year": 1994, "tags": ["playstation", "low-poly", "tech", "gradient"], "font": "\"Eurostile\", \"Rajdhani\", \"Share Tech Mono\", sans-serif", "featured": false}, {"num": 19, "id": "os2warp", "name": "OS/2 Warp", "era": "Desktop OS", "year": 1994, "tags": ["os2", "ibm", "bevel", "blue"], "font": "\"Helvetica\", \"WarpSans\", \"Arial\", sans-serif", "featured": false}, {"num": 20, "id": "macos9", "name": "Mac OS 9 Platinum", "era": "Desktop OS", "year": 1999, "tags": ["mac", "platinum", "pinstripe", "grey"], "font": "\"Charcoal\", \"Geneva\", \"Lucida Grande\", sans-serif", "featured": false}, {"num": 21, "id": "web20", "name": "Web 2.0 Glossy", "era": "Web/UI", "year": 2005, "tags": ["web2.0", "glossy", "reflection", "rounded"], "font": "\"Lucida Grande\", \"Trebuchet MS\", \"Helvetica Neue\", Arial, sans-serif", "featured": false}, {"num": 22, "id": "gameboy", "name": "Game Boy DMG", "era": "Gaming", "year": 1989, "tags": ["gameboy", "green", "lcd", "4-shade"], "font": "\"Press Start 2P\", \"VT323\", \"Courier New\", monospace", "featured": true}, {"num": 23, "id": "braun", "name": "Braun / Dieter Rams", "era": "Design", "year": 1960, "tags": ["braun", "functional", "minimal", "industrial"], "font": "\"Akzidenz-Grotesk\", \"Helvetica Neue\", Helvetica, \"Arial\", sans-serif", "featured": false}, {"num": 24, "id": "tron", "name": "Tron Vector", "era": "Sci-Fi", "year": 1982, "tags": ["tron", "vector", "cyan", "grid"], "font": "\"Orbitron\", \"Eurostile\", \"Share Tech Mono\", monospace", "featured": true}, {"num": 25, "id": "vhs", "name": "VHS Tracking", "era": "Analog", "year": 1980, "tags": ["vhs", "glitch", "scanline", "analog"], "font": "\"VT323\", \"Courier New\", monospace", "featured": false}, {"num": 26, "id": "riso", "name": "Risograph", "era": "Print", "year": 1986, "tags": ["riso", "print", "duotone", "grain"], "font": "\"Helvetica Neue\", \"Akzidenz-Grotesk\", \"Arial\", sans-serif", "featured": true}, {"num": 27, "id": "ibm3270", "name": "IBM 3270 Mainframe", "era": "Terminal", "year": 1971, "tags": ["ibm", "mainframe", "terminal", "cics"], "font": "\"IBM 3270\", \"PxPlus 3270\", \"VT323\", \"Courier New\", monospace", "featured": false}, {"num": 28, "id": "nethack", "name": "NetHack ASCII", "era": "Terminal", "year": 1987, "tags": ["ascii", "roguelike", "terminal", "mono"], "font": "\"Px437 IBM VGA\", \"Perfect DOS VGA 437\", \"VT323\", \"Courier New\", monospace", "featured": false}, {"num": 29, "id": "templeos", "name": "TempleOS", "era": "Desktop OS", "year": 2013, "tags": ["templeos", "16-color", "vga", "mono"], "font": "\"Px437 IBM VGA 8x16\", \"Perfect DOS VGA 437\", \"VT323\", \"Courier New\", monospace", "featured": false}, {"num": 30, "id": "bbsansi", "name": "BBS ANSI Art", "era": "Terminal", "year": 1989, "tags": ["bbs", "ansi", "block", "16-color"], "font": "\"Px437 IBM VGA 8x16\", \"Perfect DOS VGA 437\", \"VT323\", \"Courier New\", monospace", "featured": false}, {"num": 31, "id": "mc", "name": "Midnight Commander", "era": "Terminal", "year": 1994, "tags": ["tui", "blue", "filemanager", "ncurses"], "font": "\"Px437 IBM VGA 8x16\", \"Perfect DOS VGA 437\", \"VT323\", \"Courier New\", monospace", "featured": false}, {"num": 32, "id": "matrix", "name": "Matrix Rain", "era": "Sci-Fi", "year": 1999, "tags": ["matrix", "green", "code", "rain"], "font": "\"Matrix Code NFI\", \"MS Mincho\", \"MS Gothic\", \"Courier New\", monospace", "featured": false}, {"num": 33, "id": "btop", "name": "btop Meters", "era": "Terminal", "year": 2021, "tags": ["tui", "monitor", "gradient", "meters"], "font": "\"Hack\", \"JetBrains Mono\", \"Cascadia Code\", \"Fira Code\", \"Consolas\", monospace", "featured": false}, {"num": 34, "id": "c64", "name": "Commodore 64 BASIC", "era": "Terminal", "year": 1982, "tags": ["c64", "blue", "petscii", "basic"], "font": "\"C64 Pro\", \"Commodore 64\", \"Px437 PETSCII\", \"Press Start 2P\", monospace", "featured": false}, {"num": 35, "id": "flat2013", "name": "Flat Design 2013", "era": "Web/UI", "year": 2013, "tags": ["flat", "ios7", "minimal", "bright"], "font": "\"Helvetica Neue Light\", \"Helvetica Neue\", Helvetica, Arial, sans-serif", "featured": false}, {"num": 36, "id": "glass", "name": "Glassmorphism", "era": "Web/UI", "year": 2020, "tags": ["glass", "blur", "frosted", "modern"], "font": "\"Inter\", \"SF Pro Display\", \"Segoe UI\", system-ui, sans-serif", "featured": false}, {"num": 37, "id": "neumorph", "name": "Neumorphism", "era": "Web/UI", "year": 2020, "tags": ["neumorph", "soft", "shadow", "mono"], "font": "\"Inter\", \"SF Pro\", \"Segoe UI\", system-ui, sans-serif", "featured": false}, {"num": 38, "id": "blueprint", "name": "Blueprint / CAD", "era": "Technical", "year": 1980, "tags": ["blueprint", "cad", "grid", "cyan"], "font": "\"Helvetica Neue\", Arial, sans-serif", "featured": false}, {"num": 39, "id": "clay", "name": "Claymorphism", "era": "Web/UI", "year": 2021, "tags": ["clay", "3d", "soft", "playful"], "font": "\"Nunito\", \"SF Pro Rounded\", \"Helvetica Neue\", system-ui, sans-serif", "featured": false}, {"num": 40, "id": "brutalist", "name": "Brutalist Web", "era": "Web/UI", "year": 2016, "tags": ["brutalist", "raw", "mono", "highcontrast"], "font": "\"Times New Roman\", Times, serif", "featured": false}, {"num": 41, "id": "swiss", "name": "Swiss Style", "era": "Design", "year": 1950, "tags": ["swiss", "grid", "helvetica", "minimal"], "font": "\"Helvetica Neue\", \"Akzidenz-Grotesk\", Helvetica, Arial, sans-serif", "featured": true}, {"num": 42, "id": "bauhaus", "name": "Bauhaus", "era": "Design", "year": 1919, "tags": ["bauhaus", "primary", "geometric", "modernist"], "font": "\"Futura\", \"Futura PT\", \"Century Gothic\", \"Avenir Next\", sans-serif", "featured": false}, {"num": 43, "id": "popart", "name": "Pop Art", "era": "Art", "year": 1960, "tags": ["popart", "halftone", "primary", "comic"], "font": "\"Bungee\", \"Impact\", \"Arial Black\", sans-serif", "featured": false}, {"num": 44, "id": "opart", "name": "Op Art", "era": "Art", "year": 1964, "tags": ["opart", "bw", "illusion", "pattern"], "font": "\"Helvetica Neue\", Helvetica, Arial, sans-serif", "featured": false}, {"num": 45, "id": "hypnagogic", "name": "Hypnagogic", "era": "Aesthetic", "year": 2015, "tags": ["dreamy", "gradient", "surreal", "soft"], "font": "\"Times New Roman\", \"Georgia\", serif", "featured": false}, {"num": 46, "id": "zen", "name": "Monochrome Zen", "era": "Design", "year": 2010, "tags": ["mono", "zen", "minimal", "calm"], "font": "\"Söhne\", \"Inter\", \"Helvetica Neue\", sans-serif", "featured": false}, {"num": 47, "id": "browser", "name": "Default Browser", "era": "Web", "year": 1994, "tags": ["html", "unstyled", "timesnewroman", "default"], "font": "\"Times New Roman\", Times, serif", "featured": false}, {"num": 48, "id": "wireframe", "name": "Wireframe Sketch", "era": "Technical", "year": 2010, "tags": ["wireframe", "sketch", "lofi", "grey"], "font": "\"Kalam\", \"Comic Sans MS\", cursive", "featured": false}, {"num": 49, "id": "glitch", "name": "Glitch Databend", "era": "Aesthetic", "year": 2010, "tags": ["glitch", "databend", "rgb", "corrupt"], "font": "\"Space Mono\", \"JetBrains Mono\", \"IBM Plex Mono\", \"Courier New\", monospace", "featured": false}, {"num": 50, "id": "y2k", "name": "Y2K Chrome", "era": "Aesthetic", "year": 2000, "tags": ["y2k", "chrome", "metallic", "bubble"], "font": "\"Neue Haas Grotesk\", \"Helvetica Neue\", Arial, sans-serif", "featured": false}, {"num": 51, "id": "duotone", "name": "Duotone Poster", "era": "Print", "year": 2015, "tags": ["duotone", "poster", "highcontrast", "bold"], "font": "\"Futura\", \"Helvetica Neue\", \"Akzidenz-Grotesk\", sans-serif", "featured": false}, {"num": 52, "id": "gridpaper", "name": "Grid Paper", "era": "Technical", "year": 1980, "tags": ["grid", "paper", "graph", "engineering"], "font": "\"Shadows Into Light\", \"Architects Daughter\", \"Comic Sans MS\", cursive", "featured": false}, {"num": 53, "id": "maximalist", "name": "Maximalist 90s Banner", "era": "Web", "year": 1997, "tags": ["maximalist", "banner", "loud", "90s"], "font": "\"Comic Sans MS\", \"Trebuchet MS\", Verdana, sans-serif", "featured": false}];
  var ROLES = ["bg", "surface", "ink", "muted", "border", "accent", "accent2", "highlight", "onaccent"];
  var FEATURED = ["crt", "vaporwave", "win95", "arcade", "tron", "gameboy", "riso", "swiss"];

  function byId(id) {
    for (var i = 0; i < SYSTEMS.length; i++) if (SYSTEMS[i].id === id) return SYSTEMS[i];
    return null;
  }
  function apply(el, id) {
    var s = byId(id);
    if (!s) throw new Error("Retro: unknown system " + id);
    ROLES.forEach(function (r) { el.style.setProperty("--ui-" + r, "var(--" + id + "-" + r + ")"); });
    el.style.fontFamily = s.font;
    el.setAttribute("data-system", id);
    return s;
  }
  function reset(el) {
    ROLES.forEach(function (r) { el.style.removeProperty("--ui-" + r); });
    el.style.removeProperty("font-family");
    el.removeAttribute("data-system");
  }
  function h(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function computed(ctx, prop) {
    var p = h("span");
    p.style.color = "var(" + prop + ")";
    p.style.display = "none";
    ctx.appendChild(p);
    var c = getComputedStyle(p).color;
    ctx.removeChild(p);
    return c;
  }
  function rgb(c) {
    var m = (c.match(/[\d.]+/g) || [0, 0, 0]).map(Number);
    return { r: m[0], g: m[1], b: m[2], a: m.length > 3 ? m[3] : 1 };
  }
  function hex(c) {
    var o = rgb(c);
    var x = "#" + [o.r, o.g, o.b].map(function (v) { return ("0" + Math.round(v).toString(16)).slice(-2); }).join("");
    return o.a < 1 ? x + " " + Math.round(o.a * 100) + "%" : x;
  }
  function over(f, b) {
    return { r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 };
  }
  function lum(o) {
    function ch(v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * ch(o.r) + 0.7152 * ch(o.g) + 0.0722 * ch(o.b);
  }
  /* WCAG ratio of role fg on role ground for system id; translucent grounds sit on bg */
  function contrast(id, fg, ground) {
    var ctx = document.body;
    var base = rgb(computed(ctx, "--" + id + "-bg"));
    var g = rgb(computed(ctx, "--" + id + "-" + ground));
    if (g.a < 1) g = over(g, base);
    var f = rgb(computed(ctx, "--" + id + "-" + fg));
    if (f.a < 1) f = over(f, g);
    var a = lum(f), b = lum(g);
    return Math.round(((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)) * 100) / 100;
  }
  function gradeOf(r) { return r >= 4.5 ? "AA" : r >= 3 ? "large only" : "fails"; }

  function RetroWindow(el, props) {
    props = props || {};
    var stage = h("div", "rt-stage");
    if (props.system) apply(stage, props.system);
    var win = h("div", "rt-win");
    var bar = h("div", "rt-bar");
    var title = h("span", "rt-bar-title", props.title || "Untitled");
    var btns = h("span", "rt-bar-btns");
    btns.setAttribute("aria-hidden", "true");
    btns.appendChild(h("i")); btns.appendChild(h("i")); btns.appendChild(h("i"));
    bar.appendChild(title); bar.appendChild(btns);
    var body = h("div", "rt-body");
    body.appendChild(h("p", "rt-text", props.text || "Loop locked. 140 BPM. Twelve clips rendered to the bin."));
    body.appendChild(h("p", "rt-muted", props.caption || "Last render 00:04:12 ago"));
    var row = h("div", "rt-row");
    row.appendChild(h("button", "rt-btn rt-primary", "Render"));
    row.appendChild(h("button", "rt-btn", "Cancel"));
    var input = h("input", "rt-input");
    input.value = "140";
    input.setAttribute("aria-label", "BPM");
    row.appendChild(input);
    body.appendChild(row);
    var keys = h("div", "rt-keys");
    [["accent", "Accent"], ["accent2", "Accent 2"], ["highlight", "Highlight"]].forEach(function (k) {
      var s = h("span", "rt-key");
      var d = h("i", "rt-dot");
      d.style.background = "var(--ui-" + k[0] + ")";
      s.appendChild(d); s.appendChild(document.createTextNode(k[1]));
      keys.appendChild(s);
    });
    body.appendChild(keys);
    win.appendChild(bar); win.appendChild(body);
    stage.appendChild(win);
    stage._title = title;
    el.appendChild(stage);
    return stage;
  }

  function SystemSwitcher(el, props) {
    props = props || {};
    var wrap = h("div", "rt-switch");
    var controls = h("div", "rt-controls");
    var label = h("label", "rt-label", "System");
    var sel = h("select");
    sel.id = "rt-sel-" + Math.random().toString(36).slice(2, 7);
    label.setAttribute("for", sel.id);
    var eras = [];
    SYSTEMS.forEach(function (s) { if (eras.indexOf(s.era) < 0) eras.push(s.era); });
    eras.forEach(function (era) {
      var g = h("optgroup"); g.label = era;
      SYSTEMS.forEach(function (s) {
        if (s.era !== era) return;
        var o = h("option", null, s.num + ". " + s.name + (s.featured ? "  \u2605" : ""));
        o.value = s.id; g.appendChild(o);
      });
      sel.appendChild(g);
    });
    var prev = h("button", "rt-step", "\u25C0"); prev.setAttribute("aria-label", "Previous system");
    var next = h("button", "rt-step", "\u25B6"); next.setAttribute("aria-label", "Next system");
    var count = h("span", "rt-count");
    controls.appendChild(label); controls.appendChild(sel); controls.appendChild(prev); controls.appendChild(next); controls.appendChild(count);
    var split = h("div", "rt-split");
    var left = h("div", "rt-left");
    var stage = RetroWindow(left, {});
    var info = h("div", "rt-info");
    var name = h("h3");
    var metaLine = h("p", "rt-meta");
    var fontLine = h("p", "rt-code");
    var strip = h("div", "rt-strip");
    var ratios = h("p", "rt-meta");
    info.appendChild(name); info.appendChild(metaLine); info.appendChild(strip); info.appendChild(ratios); info.appendChild(fontLine);
    split.appendChild(left); split.appendChild(info);
    wrap.appendChild(controls); wrap.appendChild(split);
    el.appendChild(wrap);

    var current = null;
    function set(id) {
      var s = apply(stage, id);
      current = s;
      stage._title.textContent = s.name + (s.year ? " \u2014 " + s.year : "");
      sel.value = id;
      count.textContent = s.num + " / " + SYSTEMS.length + (s.featured ? " \u00B7 native theme" : "");
      name.textContent = s.name;
      metaLine.textContent = s.era + (s.year ? " \u00B7 " + s.year : "") + " \u00B7 " + s.tags.join(", ");
      fontLine.textContent = "font-family: " + s.font;
      strip.textContent = "";
      ROLES.forEach(function (r) {
        var cell = h("div", "rt-sw");
        var chip = h("b"); chip.style.background = "var(--" + id + "-" + r + ")";
        var txt = h("span");
        txt.appendChild(h("span", "rt-role", r));
        txt.appendChild(h("span", "rt-hex", hex(computed(document.body, "--" + id + "-" + r))));
        cell.appendChild(chip); cell.appendChild(txt);
        strip.appendChild(cell);
      });
      var a = contrast(id, "ink", "surface"), m = contrast(id, "muted", "surface");
      ratios.textContent = "ink on surface " + a + ":1 " + gradeOf(a) + " \u00B7 muted on surface " + m + ":1 " + gradeOf(m);
      if (props.onChange) props.onChange(s);
    }
    function step(d) {
      var i = SYSTEMS.indexOf(current);
      set(SYSTEMS[(i + d + SYSTEMS.length) % SYSTEMS.length].id);
    }
    sel.addEventListener("change", function () { set(sel.value); });
    prev.addEventListener("click", function () { step(-1); });
    next.addEventListener("click", function () { step(1); });
    set(props.initial && byId(props.initial) ? props.initial : SYSTEMS[0].id);
    return { set: set, get: function () { return current; } };
  }

  function PaletteGrid(el, props) {
    props = props || {};
    var t = h("table", "rt-grid");
    var thead = h("thead"), hr = h("tr");
    ["#", "System", "Era", "Year"].concat(ROLES).concat(["ink / surface"]).forEach(function (c) { hr.appendChild(h("th", null, c)); });
    thead.appendChild(hr); t.appendChild(thead);
    var tb = h("tbody");
    SYSTEMS.forEach(function (s) {
      var tr = h("tr");
      tr.appendChild(h("td", "rt-num", String(s.num)));
      tr.appendChild(h("td", "rt-name", s.name + (s.featured ? " \u2605" : "")));
      tr.appendChild(h("td", null, s.era));
      tr.appendChild(h("td", null, s.year ? String(s.year) : ""));
      ROLES.forEach(function (r) {
        var td = h("td", "sw"), i = h("i");
        i.style.background = "var(--" + s.id + "-" + r + ")";
        i.title = s.id + "-" + r + "  " + hex(computed(document.body, "--" + s.id + "-" + r));
        td.appendChild(i); tr.appendChild(td);
      });
      var c = contrast(s.id, "ink", "surface");
      tr.appendChild(h("td", "rt-num", c + ":1"));
      if (props.onSelect) { tr.tabIndex = 0; tr.addEventListener("click", function () { props.onSelect(s); }); }
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    el.appendChild(t);
    return t;
  }

  window.Retro = {
    systems: SYSTEMS, roles: ROLES, featured: FEATURED,
    apply: apply, reset: reset, byId: byId, contrast: contrast,
    RetroWindow: RetroWindow, SystemSwitcher: SystemSwitcher, PaletteGrid: PaletteGrid
  };
})();
