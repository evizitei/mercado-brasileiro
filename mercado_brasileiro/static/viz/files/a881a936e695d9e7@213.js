// https://observablehq.com/@d3/bubble-map@213
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["counties-albers-10m.json", new URL("br-states.json", import.meta.url)], ["population.json", new URL("beb56a2d9534662123fa352ffff2db8472e481776fcc1608ee4adbd532ea9ccf2f1decc004d57adc76735478ee68c0fd18931ba01fc859ee4901deb1bee2ed1b", import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function (md) {
    return (
      md`# Brazil Product Customer Population

Estimated population by estado Data: [Kaggle Dataset](https://www.kaggle.com/olistbr/brazilian-ecommerce?select=olist_geolocation_dataset.csv)`
    )
  });
  main.variable(observer("chart")).define("chart", ["d3", "topojson", "br", "path", "radius", "data", "format",
    "projection", "width", "height", "bounds", "center", "distance", "scale"],
    function (d3, topojson, br, path, radius, data, format, projection, width, height, bounds, center, distance, scale) {
      const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height]);

      svg.append("path")
        .datum(topojson.feature(br, br.objects.estados))
        .attr("fill", "#ddd")
        .attr("stroke", "white")
        .attr("stroke-linejoin", "round")
        .attr("d", path);

      // projection.scale(scale).center(center);

      svg.append("path")
        .datum(topojson.mesh(br, br.objects.estados, (a, b) => a !== b))
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-linejoin", "round")
        .attr("d", path);

      // svg.append("path")
      //   .datum(topojson.mesh(br, br.objects.estados, (a, b) => a !== b))
      //   // .attr("fill", "#ddd")
      //   .attr("stroke", "black")
      //   .attr("stroke-linejoin", "round")
      //   .attr("d", path);

      const legend = svg.append("g")
        .attr("fill", "#777")
        .attr("transform", "translate(700,408)")
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
  main.variable(observer("data")).define("data", ["FileAttachment", "features", "path"], async function (FileAttachment, features, path) {
    return (
      (await FileAttachment("population.json").json()).slice(1).map(([population, state, county]) => {
        const id = county;
        const feature = features.get(id);
        return {
          id,
          position: feature && path.centroid(feature),
          title: feature && feature.properties.nome,
          value: +population
        };
      })
    )
  });

  main.variable(observer("radius")).define("radius", ["d3", "data"], function (d3, data) {
    return (
      d3.scaleSqrt([0, d3.max(data, d => d.value)], [0, 30])
    )
  });

  main.variable(observer("width")).define("width", [], function () {
    return (
      975
    )
  });

  main.variable(observer("height")).define("height", [], function () {
    return (
      610
    )
  });

  main.variable(observer("projection")).define("projection", ["d3", "width", "height", "scale", "center"], function (d3, width, height, scale, center) {
    return (
      d3.geoMercator().translate([width, height / 10]).scale(600)
    )
  });

  main.variable(observer("bounds")).define("bounds", ["d3", "topojson"], function (d3, topojson) {
    return (
      d3.geoBounds(topojson)
    )
  });

  main.variable(observer("center")).define("center", ["d3", "topojson"], function (d3, topojson) {
    return (
      d3.geoCentroid(topojson)
    )
  });

  main.variable(observer("distance")).define("distance", ["d3", "bounds"], function (d3, bounds) {
    return (
      d3.geoDistance(bounds[0], bounds[1])
    )
  });

  main.variable(observer("scale")).define("scale", ["height", "distance"], function (height, distance) {
    return (
      height / distance / Math.sqrt(2)
    )
  });

  main.variable(observer("features")).define("features", ["topojson", "br"], function (topojson, br) {
    return (
      new Map(topojson.feature(br, br.objects.estados).features.map(d => [d.id, d]))
    )
  });

  main.variable(observer("path")).define("path", ["d3", "projection"], function (d3, projection) {
    return (
      d3.geoPath().projection(projection)
    )
  });
  main.variable(observer("format")).define("format", ["d3"], function (d3) {
    return (
      d3.format(",.0f")
    )
  });
  main.variable(observer("br")).define("br", ["FileAttachment"], function (FileAttachment) {
    return (
      FileAttachment("counties-albers-10m.json").json()
    )
  });
  main.variable(observer("topojson")).define("topojson", ["require"], function (require) {
    return (
      require("topojson-client@3")
    )
  });
  main.variable(observer("d3")).define("d3", ["require"], function (require) {
    return (
      require("d3@6")
    )
  });
  return main;
}
