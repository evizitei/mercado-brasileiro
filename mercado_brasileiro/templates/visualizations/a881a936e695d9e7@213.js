// https://observablehq.com/@d3/bubble-map@213
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["counties-albers-10m.json",new URL("./files/6b1776f5a0a0e76e6428805c0074a8f262e3f34b1b50944da27903e014b409958dc29b03a1c9cc331949d6a2a404c19dfd0d9d36d9c32274e6ffbc07c11350ee",import.meta.url)],["population.json",new URL("./files/beb56a2d9534662123fa352ffff2db8472e481776fcc1608ee4adbd532ea9ccf2f1decc004d57adc76735478ee68c0fd18931ba01fc859ee4901deb1bee2ed1b",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function(md){return(
md`# Bubble Map

Estimated population by county, 2016. Data: [American Community Survey](https://api.census.gov/data/2016/acs/acs5/cprofile/examples.html)`
)});
  main.variable(observer("chart")).define("chart", ["d3","topojson","us","path","radius","data","format"], function(d3,topojson,us,path,radius,data,format)
{
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, 975, 610]);

  svg.append("path")
      .datum(topojson.feature(us, us.objects.nation))
      .attr("fill", "#ddd")
      .attr("d", path);

  svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, (a, b) => a !== b))
      .attr("fill", "none")
      .attr("stroke", "white")
      .attr("stroke-linejoin", "round")
      .attr("d", path);

  const legend = svg.append("g")
      .attr("fill", "#777")
      .attr("transform", "translate(915,608)")
      .attr("text-anchor", "middle")
      .style("font", "10px sans-serif")
    .selectAll("g")
      .data(radius.ticks(4).slice(1))
    .join("g");

  legend.append("circle")
      .attr("fill", "none")
      .attr("stroke", "#ccc")
      .attr("cy", d => -radius(d))
      .attr("r", radius);

  legend.append("text")
      .attr("y", d => -2 * radius(d))
      .attr("dy", "1.3em")
      .text(radius.tickFormat(4, "s"));

  svg.append("g")
      .attr("fill", "brown")
      .attr("fill-opacity", 0.5)
      .attr("stroke", "#fff")
      .attr("stroke-width", 0.5)
    .selectAll("circle")
    .data(data
        .filter(d => d.position)
        .sort((a, b) => d3.descending(a.value, b.value)))
    .join("circle")
      .attr("transform", d => `translate(${d.position})`)
      .attr("r", d => radius(d.value))
    .append("title")
      .text(d => `${d.title}
${format(d.value)}`);

  return svg.node();
}
);
  main.variable(observer("data")).define("data", ["FileAttachment","features","path"], async function(FileAttachment,features,path){return(
(await FileAttachment("population.json").json()).slice(1).map(([population, state, county]) => {
  const id = state + county;
  const feature = features.get(id);
  return {
    id,
    position: feature && path.centroid(feature),
    title: feature && feature.properties.name,
    value: +population
  };
})
)});
  main.variable(observer("radius")).define("radius", ["d3","data"], function(d3,data){return(
d3.scaleSqrt([0, d3.max(data, d => d.value)], [0, 40])
)});
  main.variable(observer("features")).define("features", ["topojson","us"], function(topojson,us){return(
new Map(topojson.feature(us, us.objects.counties).features.map(d => [d.id, d]))
)});
  main.variable(observer("path")).define("path", ["d3"], function(d3){return(
d3.geoPath()
)});
  main.variable(observer("format")).define("format", ["d3"], function(d3){return(
d3.format(",.0f")
)});
  main.variable(observer("us")).define("us", ["FileAttachment"], function(FileAttachment){return(
FileAttachment("counties-albers-10m.json").json()
)});
  main.variable(observer("topojson")).define("topojson", ["require"], function(require){return(
require("topojson-client@3")
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@6")
)});
  return main;
}
