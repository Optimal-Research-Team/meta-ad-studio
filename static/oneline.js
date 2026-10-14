// Shared renderer for the one-sentence rounds. The page sets window.ROUND = {data: "R2", dir: "r2"} and loads its data file first.
(function () {
  const R = window.ROUND, ADS = window[R.data];
  document.body.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <symbol id="sym" viewBox="0 0 864 864"><g fill="currentColor"><circle cx="177" cy="422" r="145"/><circle cx="318" cy="147" r="115"/><circle cx="309" cy="707" r="124"/><circle cx="599" cy="146" r="92"/><circle cx="598" cy="707" r="101"/><circle cx="757" cy="329" r="74"/><circle cx="757" cy="515" r="74"/></g></symbol>
    <symbol id="arr" viewBox="0 0 24 24"><path d="M4.5 12h14M13 6.5l5.5 5.5-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  </defs></svg>`);
  const md = s => String(s).replace(/\|/g, "<br>").replace(/\{(.+?)\}/g, '<span class="nw">$1</span>').replace(/\*(.+?)\*/g, "<em>$1</em>");
  const use = id => `<svg aria-hidden="true"><use href="#${id}"/></svg>`;
  const frame = (a, f) => {
    const size = f === "post" ? "4x5" : "9x16";
    const out = a.card ? `${R.dir}/${a.svc}/${a.id}_card${a.card}` : `${R.dir}/${a.svc}/${a.id}_${size}`;
    const style = (f === "story" && a.st ? `top:${a.st}px;` : "") +
      (a.w ? `max-width:${a.w}px;${a.align === "right" ? "left:auto" : a.align === "center" ? "margin:0 auto" : ""}` : "");
    return `<div class="frame ${f}" data-out="${out}" data-tone="${a.tone}" data-box="${a.box ? 1 : 0}">
      <div class="bg"><img src="assets/${R.dir}/${a.img}_${size}.jpg" style="object-position:${(a.pos && a.pos[f]) || "50% 50%"}"></div>
      ${a.veil ? `<div class="veil ${a.tone} ${a.align || ""}"></div>` : ""}
      <div class="txt ${a.tone} ${a.align || ""} ${a.box ? "box" : ""} ${(a.at && a.at[f]) || ""}" style="${style}"><span class="mark">${use("sym")}Optimal</span><h2 class="s" style="${a.fs ? `font-size:${a.fs}px` : ""}">${md(a.s)}</h2></div>
      ${a.card && a.card < 5 ? `<span class="next ${a.tone === "light" ? "light" : "dark"}">${use("arr")}</span>` : ""}
    </div>`;
  };
  const only = new URLSearchParams(location.search).get("only");
  document.getElementById("root").innerHTML = ADS
    .filter(a => !only || only.split(",").includes(a.id))
    .map(a => a.card ? frame(a, "post") : frame(a, "post") + frame(a, "story")).join("");
})();
