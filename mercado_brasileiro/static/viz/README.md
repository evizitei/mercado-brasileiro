# Bubble Map

https://observablehq.com/@d3/bubble-map@213

View this notebook in your browser by running a web server in this folder. For
example:

~~~sh
python -m SimpleHTTPServer
~~~

Or, use the [Observable Runtime](https://github.com/observablehq/runtime) to
import this module directly into your application. To npm install:

~~~sh
npm install @observablehq/runtime@4
npm install https://api.observablehq.com/@d3/bubble-map.tgz?v=3
~~~

Then, import your notebook and the runtime as:

~~~js
import {Runtime, Inspector} from "@observablehq/runtime";
import define from "@d3/bubble-map";
~~~

To log the value of the cell named “foo”:

~~~js
const runtime = new Runtime();
const main = runtime.module(define);
main.value("foo").then(value => console.log(value));
~~~

# Projection Code

https://gist.github.com/LuisSevillano/0d0067c23463c95cc3b4d5f2633bdde0

# Flaticons
Perfume: https://www.freepik.com/

# Dropdown

https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_js_dropdown_filter